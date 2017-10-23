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

from nti.analytics_database.interfaces import IAnalyticsNTIIDFinder

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.resource_views import UserFileUploadViewEvents

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestResourceViews(AnalyticsDatabaseTest):

    def test_coverage(self):
        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        ufu = UserFileUploadViewEvents(file_view_id=2,
                                       file_ds_id=2,
                                       file_mime_type_id=1)
        self.session.add(ufu)
        self.session.commit()

        assert_that(ufu.mime_type, is_('text/x-python'))

        fileobj = fudge.Fake()
        finder = fudge.Fake().provides("find").returns(fileobj)
        component.getGlobalSiteManager().registerUtility(finder,
                                                         IAnalyticsNTIIDFinder)
        assert_that(ufu.FileObject, is_(fileobj))
        component.getGlobalSiteManager().unregisterUtility(finder,
                                                           IAnalyticsNTIIDFinder)
