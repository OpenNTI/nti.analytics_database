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

import fudge

from zope import component

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestUsers(AnalyticsDatabaseTest):

    def test_intid_identifier(self):
        fake = fudge.Fake()
        intid = fudge.Fake().provides("get_object").returns(fake)
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)
        user = Users()
        user.user_ds_id = 1
        assert_that(user,
                    has_property('user', is_(fake)))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
