#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,no-member

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that

import fudge

from zope import component

from nti.analytics_database.interfaces import IAnalyticsNTIIDFinder
from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.resources import Resources

from nti.analytics_database.resource_views import VideoPlaySpeedEvents
from nti.analytics_database.resource_views import UserFileUploadViewEvents

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestResourceViews(AnalyticsDatabaseTest):

    def test_coverage(self):
        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        user = Users(user_ds_id=4, user_id=1, username=u'ichigo')
        self.session.add(user)

        upload = UserFileUploadViewEvents(file_view_id=2,
                                          file_ds_id=2,
                                          file_mime_type_id=1,
                                          creator_id=1)
        self.session.add(upload)

        resource = Resources(resource_id=1, resource_ds_id=3,
                             max_time_length=10)
        self.session.add(resource)

        event = VideoPlaySpeedEvents(video_play_speed_id=1,
                                     old_play_speed=u'slow',
                                     new_play_speed=u'fast',
                                     video_time=1,
                                     resource_id=1)
        self.session.add(event)

        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden == 4:
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(upload.mime_type, is_('text/x-python'))

        assert_that(upload.ObjectCreator, is_(fake))
        fake_creator = fudge.Fake()
        upload.ObjectCreator = fake_creator
        assert_that(upload.ObjectCreator, is_(fake_creator))

        assert_that(event.ResourceId, is_('3'))

        assert_that(event.MaxDuration, is_(10))
        event.MaxDuration = 15
        assert_that(event.MaxDuration, is_(15))
        
        assert_that(event.course_id, is_(none()))

        fileobj = fudge.Fake()
        finder = fudge.Fake().provides("find").returns(fileobj)
        component.getGlobalSiteManager().registerUtility(finder,
                                                         IAnalyticsNTIIDFinder)

        assert_that(upload.FileObject, is_(fileobj))

        component.getGlobalSiteManager().unregisterUtility(finder,
                                                           IAnalyticsNTIIDFinder)
        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
