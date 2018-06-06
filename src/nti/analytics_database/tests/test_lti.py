#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from hamcrest import assert_that
from hamcrest import is_
from hamcrest import none

import fudge

from zope import component

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier
from nti.analytics_database.lti import LTIAssetLaunches
from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestLTI(AnalyticsDatabaseTest):

    def test_coverage(self):

        from IPython.core.debugger import Tracer;Tracer()()

        launch = LTIAssetLaunches(lti_asset_launches_id=1,
                                  resource_id=1,
                                  course_id=1,
                                  user_id=1,
                                  context_path=u'a/b')
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

        assert_that(launch.AssetId, is_(None))
        assert_that(launch.ContextPath, is_(['a', 'b']))
        assert_that(launch.Title, is_(none()))

        assert_that(launch.user, is_(fake))
        fake2 = fudge.Fake()
        launch.user = fake2
        assert_that(launch.user, is_(fake2))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                         IAnalyticsIntidIdentifier)