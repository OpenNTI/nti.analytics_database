#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from nti.analytics_database.search import SearchQueries

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestSearch(AnalyticsDatabaseTest):

    def test_search_types(self):
        search = SearchQueries()
        search.search_types = 'a/b/c'
        assert_that(search,
                    has_property('SearchTypes', is_(['a', 'b', 'c'])))
