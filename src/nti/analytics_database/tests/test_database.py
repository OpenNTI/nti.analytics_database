#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

from nti.analytics_database.users import Users

from nti.analytics_database.tests import AnalyticsDatabaseTest

class TestDatabase(AnalyticsDatabaseTest):

    def test_database(self):
        count = self.session.query(Users).count()
        assert_that(count, is_(0))
        assert_that(self.engine.table_names(), has_length(1))