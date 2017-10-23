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

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.mime_types import FileMimeTypes

from nti.analytics_database.resources import Resources

from nti.analytics_database.assessments import AssignmentGrades
from nti.analytics_database.assessments import AssignmentsTaken
from nti.analytics_database.assessments import AssignmentDetails
from nti.analytics_database.assessments import AssignmentFeedback
from nti.analytics_database.assessments import SelfAssessmentViews
from nti.analytics_database.assessments import SelfAssessmentsTaken
from nti.analytics_database.assessments import AssignmentDetailGrades
from nti.analytics_database.assessments import FeedbackUserFileUploadMimeTypes

from nti.analytics_database.assessments import _load_response

from nti.analytics_database.tests import AnalyticsDatabaseTest

from nti.analytics_database.users import Users


class TestAssessments(AnalyticsDatabaseTest):

    def test_load_response(self):
        assert_that(_load_response('{"a": 1}'),
                    is_({'a': 1}))

    def test_coverage(self):
        fmt = FileMimeTypes(file_mime_type_id=1, mime_type=u'text/x-python')
        self.session.add(fmt)

        user = Users(user_ds_id=1, user_id=1, username=u'aizen')
        self.session.add(user)

        taken = AssignmentsTaken(assignment_id=u'1',
                                 submission_id=1,
                                 course_id=1,
                                 assignment_taken_id=1)
        self.session.add(taken)
        grades = AssignmentGrades(grade_id=1,
                                  assignment_taken_id=1,
                                  grade=u'A',
                                  grade_num=100,
                                  grader=1)
        self.session.add(grades)

        detail_grades = AssignmentDetailGrades(question_id=u'1',
                                               question_part_id=1,
                                               assignment_taken_id=1,
                                               assignment_details_id=1,
                                               is_correct=True,
                                               grade=u'A',
                                               grade_num=100,
                                               grader=1)
        self.session.add(detail_grades)

        details = AssignmentDetails(assignment_details_id=1,
                                    question_part_id=1,
                                    question_id=1,
                                    assignment_taken_id=1,
                                    submission='{"1": 1}',)
        self.session.add(details)

        feedback = AssignmentFeedback(feedback_ds_id=2,
                                      feedback_id=1,
                                      grade_id=1,
                                      assignment_taken_id=1)
        self.session.add(feedback)

        upload = FeedbackUserFileUploadMimeTypes(count=1,
                                                 feedback_id=1,
                                                 file_mime_type_id=1,
                                                 feedback_file_upload_mime_type_id=1)
        self.session.add(upload)

        self_taken = SelfAssessmentsTaken(submission_id=2,
                                          course_id=1,
                                          self_assessment_id=1,
                                          assignment_id=1)
        self.session.add(self_taken)

        resource = Resources(resource_id=1, resource_ds_id=3)
        self.session.add(resource)

        self_views = SelfAssessmentViews(self_assessment_view_id=1,
                                         resource_id=1,
                                         course_id=1,
                                         assignment_id=1,
                                         user_id=1,
                                         context_path=u'a/b')
        self.session.add(self_views)
        self.session.commit()

        fake = fudge.Fake()

        class MockIntId(object):
            def get_object(self, iden):
                if iden in (1, 2, 3):
                    return fake
        intid = MockIntId()
        component.getGlobalSiteManager().registerUtility(intid,
                                                         IAnalyticsIntidIdentifier)

        assert_that(taken.GradeNum, is_(100))
        assert_that(taken.Grade, is_('A'))
        assert_that(taken.Grader, is_(1))
        assert_that(taken.Submission, is_(fake))

        assert_that(details.IsCorrect, is_(True))
        assert_that(details.Answer, is_({1: 1}))
        assert_that(details.Grade, is_('A'))
        assert_that(details.Grader, is_(user))

        assert_that(grades.Grader, is_(user))
        assert_that(grades.Grade, is_('A'))

        assert_that(feedback.FileMimeTypes,
                    is_({'text/x-python': 1}))

        assert_that(self_taken.Submission, is_(fake))

        assert_that(self_views.ResourceId, is_('3'))
        assert_that(self_views.ContextPath, is_(['a', 'b']))

        assert_that(self_views.user, is_(fake))
        fake2 = fudge.Fake()
        self_views.user = fake2
        assert_that(self_views.user, is_(fake2))

        component.getGlobalSiteManager().unregisterUtility(intid,
                                                           IAnalyticsIntidIdentifier)
