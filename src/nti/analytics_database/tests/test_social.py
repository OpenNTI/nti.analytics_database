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

from nti.analytics_database.social import DynamicFriendsListsCreated
from nti.analytics_database.social import DynamicFriendsListsMemberAdded

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestSocial(AnalyticsDatabaseTest):

    def test_intsid_identifier(self):
        user = Users(user_ds_id=1, user_id=1, username=u'ichigo')
        self.session.add(user)

        dfl = DynamicFriendsListsCreated(dfl_ds_id=2, dfl_id=2)
        self.session.add(dfl)

        added = DynamicFriendsListsMemberAdded(dfl_id=dfl.dfl_id,
                                               target_id=user.user_id)
        self.session.add(added)
        self.session.commit()

        class MockIntId(object):
            def get_object(self, iden):
                if iden == 1:
                    return user
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)
        assert_that(added._target_entity, is_(user))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)

    def test_intid_identifier(self):
        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden == 1:
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)
        dfl = DynamicFriendsListsCreated(dfl_ds_id=1)
        assert_that(dfl,
                    has_property('Group', is_(fake)))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
