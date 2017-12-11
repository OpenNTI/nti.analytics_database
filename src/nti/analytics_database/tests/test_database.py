#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_length
from hamcrest import assert_that

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestDatabase(AnalyticsDatabaseTest):

    def test_database(self):
        assert_that(self.engine.table_names(), has_length(68))
