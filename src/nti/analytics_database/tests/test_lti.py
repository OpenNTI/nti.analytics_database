#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from hamcrest import assert_that
from hamcrest import is_

from nti.analytics_database.lti import LTIAssetLaunches

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestLTI(AnalyticsDatabaseTest):

    def test_event(self):

        launch = LTIAssetLaunches(user_id=1,
                                  course_id=1,
                                  context_path=u'a/b',
                                  resource_id=1,
                                  lti_asset_launches_id=1)

        self.session.add(launch)

        self.session.commit()

        assert_that(launch.ContextPath, is_(['a', 'b']))
        assert_that(launch.resource_id, is_(1))
        assert_that(launch.course_id, is_(1))
        assert_that(launch.user_id, is_(1))
        assert_that(launch.lti_asset_launches_id, is_(1))
