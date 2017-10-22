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

from datetime import datetime

from nti.analytics_database.sessions import Sessions

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestSessions(AnalyticsDatabaseTest):

    def test_duration(self):
        session = Sessions()
        now = datetime.now()
        session.end_time = session.start_time = now
        assert_that(session,
                    has_property('Duration', is_(0)))
