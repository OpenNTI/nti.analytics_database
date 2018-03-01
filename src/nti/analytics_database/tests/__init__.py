#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import unittest

from sqlalchemy import create_engine as sqlalchemy_create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy.pool import StaticPool

from nti.analytics_database import Base

from zope.component.hooks import setHooks

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

import zope.testing.cleanup


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


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.analytics_database',)

    @classmethod
    def setUp(cls):
        setHooks()
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, unused_test=None):
        setHooks()

    @classmethod
    def testTearDown(cls):
        pass


class AnalyticsDatabaseTest(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def setUp(self):
        self.engine = create_engine()
        self.metadata = getattr(Base, 'metadata')
        self.metadata.create_all(bind=self.engine)
        self.sessionmaker = create_sessionmaker(self.engine)
        self.session = create_session(self.sessionmaker)

    def tearDown(self):
        # pylint: disable=no-member
        self.metadata.drop_all(bind=self.engine)
        self.session.close()
