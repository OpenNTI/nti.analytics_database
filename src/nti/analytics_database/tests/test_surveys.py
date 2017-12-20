#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods
# pylint: disable=no-member

from hamcrest import is_
from hamcrest import assert_that

from nti.analytics_database.resources import Resources

from nti.analytics_database.surveys import SurveyViews

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestSurveys(AnalyticsDatabaseTest):

    def test_survey_views(self):
        user = Users(user_ds_id=1, user_id=1, username=u'ichigo')
        self.session.add(user)

        resource = Resources(resource_id=1, resource_ds_id=2,
                             max_time_length=10)
        self.session.add(resource)

        survey = SurveyViews(survey_view_id=1, resource_id=1,
                             time_length=1,
                             course_id=1, survey_id=1, user_id=1)
        self.session.add(survey)
        self.session.commit()

        assert_that(survey.ResourceId, is_('2'))
