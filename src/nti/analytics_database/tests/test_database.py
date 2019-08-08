#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import equal_to

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.database import _make_safe_for_logging


class TestDatabase(AnalyticsDatabaseTest):

    def test_database(self):
        assert_that(self.engine.table_names(), has_length(71))

    def test_no_log_password(self):
        uri = 'mysql+pymysql://ntianalytics:foobar123@db1.alpha:3306/Analytics_xyzuniversity?charset=utf8'

        assert_that(_make_safe_for_logging(uri),
                    equal_to('mysql+pymysql://ntianalytics:*********@db1.alpha:3306/Analytics_xyzuniversity?charset=utf8'))

        uri = 'gevent_mysql://ntianalytics:foobar123@db1.alpha:3306/Analytics_ENGAGE?charset=utf8'
        assert_that(_make_safe_for_logging(uri),
                    equal_to('gevent_mysql://ntianalytics:*********@db1.alpha:3306/Analytics_ENGAGE?charset=utf8'))
