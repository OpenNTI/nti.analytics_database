#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import os
import unittest
import importlib

from sqlalchemy import create_engine as sqlalchemy_create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy.pool import StaticPool

from nti.analytics_database import Base


def _import_db_modules():
    """
    Import modules to create database
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    files = [os.path.splitext(f)[0] for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f)) and f.endswith('.py')]
    for name in files:
        name = "nti.analytics_database.%s" % name
        importlib.import_module(name)
_import_db_modules()
del _import_db_modules


def create_engine(dburi='sqlite://'):
    result = sqlalchemy_create_engine(dburi)
    return result


def create_sessionmaker(engine, autoflush=False, twophase=False):
    result = sessionmaker(bind=engine,
                          autoflush=autoflush,
                          twophase=twophase)
    return result


def create_session(session_maker):
    return scoped_session(session_maker)


class AnalyticsDatabaseTest(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine()
        self.metadata = getattr(Base, 'metadata')
        self.metadata.create_all(bind=self.engine)
        self.sessionmaker = create_sessionmaker(self.engine)
        self.session = create_session(self.sessionmaker)

    def tearDown(self):
        # pylint: disable=no-member
        self.session.close()
