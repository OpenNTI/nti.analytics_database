#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from hamcrest import assert_that
from hamcrest import is_

import fudge

from zope import component

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier
from nti.analytics_database.lti import LTIAssetLaunches
from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestLTI(AnalyticsDatabaseTest):

    def test_coverage(self):

        launch = LTIAssetLaunches(lti_asset_launch_id=1,
                                  lti_asset_launch_id_seq=1)
        self.session.add(launch)

        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden in (1,):
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(launch.lti_tool_launches_id, is_(fake))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                         IAnalyticsIntidIdentifier)