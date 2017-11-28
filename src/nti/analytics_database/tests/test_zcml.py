#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_property

import os
import shutil
import tempfile
from six.moves import configparser

from zope import component

from nti.analytics_database.database import AnalyticsDB

from nti.analytics_database.interfaces import IAnalyticsDB

import nti.testing.base

ZCML_STRING = """
<configure	xmlns="http://namespaces.zope.org/zope"
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

            config_file = os.path.join(tmp_dir, 'analytics.cfg')
            with open(config_file, 'w') as configfile:
                config.write(configfile)

            db = AnalyticsDB(config=config_file)
            assert_that(db, has_property('twophase', is_(True)))
            assert_that(db, has_property('dburi', 'sqlite://'))
        finally:
            shutil.rmtree(tmp_dir, True)
