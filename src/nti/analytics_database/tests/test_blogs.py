#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import fudge

from zope import component

from nti.analytics_database.blogs import BlogsCreated
from nti.analytics_database.blogs import BlogCommentsCreated
from nti.analytics_database.blogs import BlogCommentsUserFileUploadMimeTypes

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestBlogs(AnalyticsDatabaseTest):

    def test_coverage(self):
        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        created = BlogsCreated(blog_ds_id=1, blog_id=1)
        self.session.add(created)

        comment = BlogCommentsCreated(comment_id=1, blog_id=1)
        self.session.add(comment)

        upload = BlogCommentsUserFileUploadMimeTypes(count=1,
                                                     comment_id=1,
                                                     file_mime_type_id=1,
                                                     blog_comment_file_upload_mime_type_id=1)
        self.session.add(upload)

        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden in (1):
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(created.Blog, is_(fake))
        assert_that(comment.Blog, is_(fake))

        assert_that(comment.FileMimeTypes,
                    is_({'text/x-python': 1}))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
