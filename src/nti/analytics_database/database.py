#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import re

from six.moves import configparser

import transaction

from six.moves import urllib_parse

from sqlalchemy import event
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy.pool import StaticPool

from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.sqlalchemy import register

from nti.analytics_database.interfaces import IAnalyticsDB

from nti.analytics_database.metadata import AnalyticsMetadata

logger = __import__('logging').getLogger(__name__)


def _make_safe_for_logging(uri):
    """
    Attempts to obscure passwords in the uri so they can't be logged
    """
    def stars(m):
        return ':'+ ('*'*len(m.group(1)))+'@'

    def _make_parts_safe(parts):
        netloc = parts[1]
        netloc = re.sub(':(.*?)@', stars, netloc)
        parts[1] = netloc
        return parts

    # Some of our uris may have invalid schemes and therefore don't
    # parse correctly with urlparse.
    parts = list(urllib_parse.urlparse(uri))
    netloc = parts[1]
    if netloc:
        parts = _make_parts_safe(parts)
    else:
        # Well that is weird we aren't valid and can't be parsed
        # we've seen this with urls that use the scheme gevent_mysql
        # replace the scheme with a valid scheme to do parsing
        orig_scheme, remaining = uri.split(':', 1)
        fixed_uri = ':'.join(['http', remaining])
        fixed_parts = list(urllib_parse.urlparse(fixed_uri))
        if fixed_parts[1]:
            parts = _make_parts_safe(fixed_parts)
            parts[0] = orig_scheme

    return urllib_parse.urlunparse(parts)


@interface.implementer(IAnalyticsDB)
class AnalyticsDB(object):

    pool_size = 30
    max_overflow = 10
    pool_recycle = 300

    def __init__(self, dburi=None, twophase=False, autocommit=False, echo=False,
                 defaultSQLite=False, testmode=False, config=None, metadata=True):
        self.dburi = dburi
        self.twophase = twophase
        self.autocommit = autocommit
        self.echo = echo
        self.testmode = testmode
        self.defaultSQLite = defaultSQLite
        if defaultSQLite and not dburi:
            data_dir = os.getenv('DATASERVER_DATA_DIR') or '/tmp'
            data_dir = os.path.expanduser(data_dir)
            data_file = os.path.join(data_dir, 'analytics-sqlite.db')
            # Default to gevent friendly sqlite driver
            # See relstorage and nti.monkey
            self.dburi = "gevent+sqlite:///%s" % data_file
        elif config:
            config_name = os.path.expandvars(config)
            parser = configparser.ConfigParser()
            parser.read([config_name])
            if parser.has_option('analytics', 'dburi'):
                self.dburi = parser.get('analytics', 'dburi')
            if parser.has_option('analytics', 'twophase'):
                self.twophase = parser.getboolean('analytics', 'twophase')
            if parser.has_option('analytics', 'autocommit'):
                self.autocommit = parser.getboolean('analytics', 'autocommit')

        if metadata:
            logger.info("Connecting to database at '%s' (twophase=%s) (testmode=%s)",
                        _make_safe_for_logging(self.dburi), self.twophase, self.testmode)
            self.metadata = AnalyticsMetadata(self.engine)
        else:
            self.metadata = None

    @Lazy
    def engine(self):
        if self.dburi == 'sqlite://':
            # In-memory connections have a different db per connection, so let's make
            # them share a db connection to avoid missing metadata issues.
            # Only for tests.
            result = create_engine(self.dburi,
                                   connect_args={'check_same_thread': False},
                                   echo=self.echo,
                                   poolclass=StaticPool)

        elif   self.dburi.startswith('sqlite') \
            or self.dburi.startswith('gevent+sqlite'):
            result = create_engine(self.dburi,
                                   echo=self.echo)

            @event.listens_for(result, "begin")
            def do_begin(conn):
                conn.execute("BEGIN DEFERRED TRANSACTION")
        else:
            result = create_engine(self.dburi,
                                   pool_size=self.pool_size,
                                   max_overflow=self.max_overflow,
                                   pool_recycle=self.pool_recycle,
                                   echo=self.echo,
                                   echo_pool=False)
        return result

    @Lazy
    def sessionmaker(self):
        if self.autocommit:
            result = sessionmaker(bind=self.engine,
                                  twophase=self.twophase)
        else:
            # The way stuff is currently architected, we *must* have
            # autoflush enabled. This will ensure queries will flush to the
            # db and have the most accurate view of state. If not, queries
            # that do not query on a primary key (most of our tables have
            # sequences for primary keys) will not find these newly added objects.
            # Thus we may have duplicate dataserver objects in the analytics
            # database.

            # Use the ZTE for transaction handling.
            result = sessionmaker(bind=self.engine,
                                  autoflush=True,
                                  twophase=self.twophase)
        return result

    @Lazy
    def session(self):
        # This session_scoped object acts as a proxy to the underlying,
        # thread-local session objects.
        result = scoped_session(self.sessionmaker)
        if self.dburi != 'sqlite://' or not self.autocommit:
            # Tests
            register(result)
        return result

    def savepoint(self):
        if not self.testmode and not self.defaultSQLite:
            return transaction.savepoint()
        return None
