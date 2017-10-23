#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from datetime import datetime

import fudge

from zope import component

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.resources import Resources

from nti.analytics_database.resource_tags import NotesViewed
from nti.analytics_database.resource_tags import NotesCreated
from nti.analytics_database.resource_tags import BookmarksCreated
from nti.analytics_database.resource_tags import HighlightsCreated
from nti.analytics_database.resource_tags import NotesUserFileUploadMimeTypes

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestResourceTags(AnalyticsDatabaseTest):

    def test_coverage(self):
        resource = Resources(resource_id=1, resource_ds_id=1)
        self.session.add(resource)

        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        user = Users(user_ds_id=2, user_id=1, username=u'ichigo')
        self.session.add(user)

        created = NotesCreated(note_ds_id=3, note_id=1, sharing=u'GLOBAL',
                               resource_id=1)
        self.session.add(created)

        viewed = NotesViewed(note_id=1, user_id=1, resource_id=1,
                             timestamp=datetime.now())
        self.session.add(viewed)

        upload = NotesUserFileUploadMimeTypes(count=1,
                                              note_id=1,
                                              file_mime_type_id=1,
                                              note_file_upload_mime_type_id=1)
        self.session.add(upload)

        highlight = HighlightsCreated(highlight_id=1, highlight_ds_id=4,
                                      resource_id=1)
        self.session.add(highlight)

        bookmark = BookmarksCreated(bookmark_id=1, bookmark_ds_id=5,
                                    resource_id=1)
        self.session.add(bookmark)

        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden in (3, 4, 5):
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(viewed.Note, is_(fake))
        viewed.Note = fake
        assert_that(viewed.Note, is_(fake))

        assert_that(created.FileMimeTypes,
                    is_({'text/x-python': 1}))

        assert_that(bookmark.Bookmark, is_(fake))
        assert_that(highlight.Highlight, is_(fake))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
