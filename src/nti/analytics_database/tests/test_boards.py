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

from nti.analytics_database.boards import TopicsCreated
from nti.analytics_database.boards import ForumsCreated
from nti.analytics_database.boards import ForumCommentsCreated
from nti.analytics_database.boards import ForumCommentsUserFileUploadMimeTypes

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestBoards(AnalyticsDatabaseTest):

    def test_coverage(self):
        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        forum_created = ForumsCreated(forum_ds_id=1, forum_id=1)
        self.session.add(forum_created)

        topic_created = TopicsCreated(topic_ds_id=2,
                                      topic_id=1,
                                      forum_id=1)
        self.session.add(topic_created)

        comment = ForumCommentsCreated(comment_id=1,
                                       topic_id=1,
                                       forum_id=1)
        self.session.add(comment)

        upload = ForumCommentsUserFileUploadMimeTypes(count=1,
                                                      comment_id=1,
                                                      file_mime_type_id=1,
                                                      comment_file_upload_mime_type_id=1)
        self.session.add(upload)

        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden in (1, 2):
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(forum_created.Forum, is_(fake))
        assert_that(forum_created.RootContext, is_(none()))  # no resolver

        fake_root = fudge.Fake()
        forum_created.RootContext = fake_root
        assert_that(forum_created.RootContext, is_(fake_root))

        assert_that(topic_created.Topic, is_(fake))

        assert_that(comment.Topic, is_(fake))

        fake2 = fudge.Fake()
        comment.Topic = fake2
        assert_that(comment.Topic, is_(fake2))

        assert_that(comment.Forum, is_(fake))
        comment.Forum = fake2
        assert_that(comment.Forum, is_(fake2))

        assert_that(comment.FileMimeTypes,
                    is_({'text/x-python': 1}))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
