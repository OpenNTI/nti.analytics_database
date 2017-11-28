#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_property

import os
import shutil
import tempfile
from six.moves import configparser

import fudge

import pymysql

from zope import component

from nti.analytics_database.database import AnalyticsDB

from nti.analytics_database.interfaces import IAnalyticsDB

import nti.testing.base

pymysql.install_as_MySQLdb()

ZCML_STRING = """
<configure    xmlns="http://namespaces.zope.org/zope"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:zcml="http://namespaces.zope.org/zcml"
            xmlns:adb="http://nextthought.com/analytics/database">

    <include package="zope.component" file="meta.zcml" />
    <include package="zope.security" file="meta.zcml" />
    <include package="zope.component" />
    <include package="." file="meta.zcml" />

    <configure>
        <adb:registerAnalyticsDB defaultSQLite="True"
                                 twophase="True"
                                 autocommit="False" />
    </configure>
</configure>

"""


class TestZcml(nti.testing.base.ConfiguringTestBase):

    def test_registration(self):
        self.configure_string(ZCML_STRING)
        db = component.queryUtility(IAnalyticsDB)
        assert_that(db, is_(not_none()))
        assert_that(db, is_(not_none()))
        assert_that(db, has_property('twophase', True))
        assert_that(db, has_property('autocommit', False))


class TestConfig(nti.testing.base.ConfiguringTestBase):

    def test_config_file(self):
        tmp_dir = tempfile.mkdtemp(dir="/tmp")
        try:
            config = configparser.RawConfigParser()
            config.add_section('analytics')
            config.set('analytics', 'dburi', 'sqlite://')
            config.set('analytics', 'twophase', 'True')
            config.set('analytics', 'autocommit', 'True')

            config_file = os.path.join(tmp_dir, 'analytics.cfg')
            with open(config_file, 'w') as configfile:
                config.write(configfile)

            db = AnalyticsDB(config=config_file)
            assert_that(db, has_property('twophase', is_(True)))
            assert_that(db, has_property('dburi', 'sqlite://'))
            assert_that(db,
                        has_property('session', is_(not_none())))
        finally:
            shutil.rmtree(tmp_dir, True)

    @fudge.patch('nti.analytics_database.database.transaction.savepoint')
    def test_mysql_config(self, mock_trax):
        mock_trax.expects_call().returns_fake()
        tmp_dir = tempfile.mkdtemp(dir="/tmp")
        try:
            config = configparser.RawConfigParser()
            config.add_section('analytics')
            config.set('analytics', 'dburi',
                       'mysql://Users:Users@myhost/Analytics')
            config.set('analytics', 'twophase', 'True')
            config.set('analytics', 'autocommit', 'False')
            config.set('analytics', 'salt', 'ichigo')

            config_file = os.path.join(tmp_dir, 'sample.cfg')
            with open(config_file, 'w') as configfile:
                config.write(configfile)

            db = AnalyticsDB(config=config_file, metadata=False)
            assert_that(db, has_property('twophase', is_(True)))
            assert_that(db, has_property('autocommit', is_(False)))
            assert_that(db,
                        has_property('dburi', 'mysql://Users:Users@myhost/Analytics'))
            assert_that(db, has_property('defaultSQLite', is_(False)))
            assert_that(db,
                        has_property('session', is_(not_none())))

            # coverage
            assert_that(db.savepoint(), is_(not_none()))
            db.testmode = True
            assert_that(db.savepoint(), is_(none()))
        finally:
            shutil.rmtree(tmp_dir, True)
