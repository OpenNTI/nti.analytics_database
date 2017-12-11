#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

import functools

from zope import schema
from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from nti.analytics_database.database import AnalyticsDB

from nti.analytics_database.interfaces import IAnalyticsDB

logger = __import__('logging').getLogger(__name__)


class IRegisterAnalyticsDB(interface.Interface):
    """
    The arguments needed for registering the analytics db.
    """
    dburi = fields.TextLine(title=u"db uri", required=False)
    twophase = schema.Bool(title=u"twophase commit", required=False)
    autocommit = fields.Bool(title=u"autocommit", required=False)
    defaultSQLite = schema.Bool(title=u"default to SQLite", required=False)
    testmode = schema.Bool(title=u"start the db in test mode", required=False)
    config = fields.TextLine(title=u"path to config file", required=False)


def registerAnalyticsDB(_context, dburi=None, twophase=False, autocommit=False,
                        defaultSQLite=False, testmode=False, config=None):
    """
    Register the db
    """
    factory = functools.partial(AnalyticsDB,
                                dburi=dburi,
                                twophase=twophase,
                                autocommit=autocommit,
                                defaultSQLite=defaultSQLite,
                                testmode=testmode,
                                config=config)
    utility(_context, provides=IAnalyticsDB, factory=factory)
