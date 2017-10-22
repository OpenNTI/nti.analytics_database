#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestDatabase(AnalyticsDatabaseTest):

    def test_database(self):
        assert_that(self.engine.table_names(), has_length(68))
