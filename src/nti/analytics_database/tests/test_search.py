#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

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
