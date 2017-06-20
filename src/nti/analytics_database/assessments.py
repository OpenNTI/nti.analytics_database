#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import json

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence

from zope import component

from nti.analytics_database import NTIID_COLUMN_TYPE
from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database import Base

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.meta_mixins import CourseMixin
from nti.analytics_database.meta_mixins import DeletedMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import ResourceMixin
from nti.analytics_database.meta_mixins import FileMimeTypeMixin

from nti.property.property import alias

class AssignmentIdMixin(object):

	AssessmentId = AssignmentId = alias( 'assignment_id' )

	@declared_attr
	def assignment_id(cls):
		return Column('assignment_id', NTIID_COLUMN_TYPE, nullable=False, index=True)

class AssignmentMixin(BaseTableMixin, CourseMixin, TimeLengthMixin, AssignmentIdMixin):
	pass

class AssignmentsTaken(Base, AssignmentMixin):
	__tablename__ = 'AssignmentsTaken'

	IsLate = alias( 'is_late' )
	Details = alias( 'details' )

	submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True, index=True, autoincrement=False)

	assignment_taken_id = Column('assignment_taken_id', Integer, Sequence('assignments_taken_seq'),
								index=True, nullable=False, primary_key=True)

	# We may have multiple grades in the future.
	grade = relationship('AssignmentGrades', uselist=False, lazy='joined')

	details = relationship('AssignmentDetails', uselist=True, lazy="select")

	is_late = Column('is_late', Boolean, nullable=True)

	@property
	def GradeNum(self):
		return self.grade and self.grade.grade_num

	@property
	def Grade(self):
		return self.grade and self.grade.grade

	@property
	def Grader(self):
		return self.grade and self.grade.grader

	@property
	def Submission(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.submission_id )

class AssignmentSubmissionMixin(BaseTableMixin):

	@declared_attr
	def assignment_taken_id(cls):
		return Column('assignment_taken_id',
					  Integer,
					  ForeignKey("AssignmentsTaken.assignment_taken_id"),
					  nullable=False,
					  index=True)

def _load_response( value ):
	"""For a database response value, transform it into a useable state."""
	response = json.loads( value )
	if isinstance( response, dict ):
		# Convert to int keys, if possible.
		# We currently do not handle mixed types of keys.
		try:
			response = {int( x ): y for x,y in response.items()}
		except ValueError:
			pass
	return response

class DetailMixin(TimeLengthMixin):

	QuestionId = alias( 'question_id' )
	QuestionPartId = alias( 'question_part_id' )

	# Counting on these parts/ids being integers.
	# Max length of 114 as of 8.1.14
	@declared_attr
	def question_id(cls):
		return Column('question_id', NTIID_COLUMN_TYPE, nullable=False, index=True)

	@declared_attr
	def question_part_id(cls):
		return Column('question_part_id', INTID_COLUMN_TYPE, nullable=False, autoincrement=False, index=True)

	@declared_attr
	def submission(cls):
		# Null if left blank
		return Column('submission', Text, nullable=True)  # (Freeform|MapEntry|Index|List)

	@property
	def Answer(self):
		return _load_response( self.submission )

class GradeMixin(object):

	Grade = alias( 'grade' )

	# Could be a lot of types: 7, 7/10, 95, 95%, A-, 90 A
	@declared_attr
	def grade(cls):
		return Column('grade', String(32), nullable=True)

	# For easy aggregation
	@declared_attr
	def grade_num(cls):
		return Column('grade_num', Float, nullable=True)

	# 'Null' for auto-graded parts.
	@declared_attr
	def grader(cls):
		return Column('grader', Integer, ForeignKey("Users.user_id"), nullable=True, index=True)

	@declared_attr
	def _grader_record(self):
		return relationship('Users', lazy="select", foreign_keys=[self.grader])

	@property
	def Grader(self):
		return self._grader_record

class GradeDetailMixin(GradeMixin):

	IsCorrect = alias( 'is_correct' )

	# For multiple choice types
	@declared_attr
	def is_correct(cls):
		return Column('is_correct', Boolean, nullable=True)

class AssignmentDetails(Base, DetailMixin, AssignmentSubmissionMixin):

	__tablename__ = 'AssignmentDetails'

	assignment_details_id = Column('assignment_details_id',
									Integer,
									Sequence('assignment_details_seq'),
									primary_key=True)
	grade = relationship('AssignmentDetailGrades', uselist=False, lazy='joined')

	@property
	def IsCorrect(self):
		return self.grade and self.grade.IsCorrect

	@property
	def Grade(self):
		return self.grade and self.grade.grade

	@property
	def Grader(self):
		return self.grade and self.grade.Grader

class AssignmentGrades(Base, AssignmentSubmissionMixin, GradeMixin):
	__tablename__ = 'AssignmentGrades'
	grade_id = Column('grade_id', Integer, Sequence('assignment_grade_id_seq'), primary_key=True, index=True)

class AssignmentDetailGrades(Base, GradeDetailMixin, AssignmentSubmissionMixin):

	__tablename__ = 'AssignmentDetailGrades'
	# We cannot use foreign keys since the parent key must be unique, and
	# we cannot have this as part of a primary key due to its size (mysql).
	question_id = Column('question_id', NTIID_COLUMN_TYPE, nullable=False)
	question_part_id = Column('question_part_id', INTID_COLUMN_TYPE, nullable=True, autoincrement=False)

	assignment_details_id = Column('assignment_details_id',
								   Integer,
								   ForeignKey("AssignmentDetails.assignment_details_id"),
								   unique=True,
								   primary_key=True)

# Each feedback 'tree' should have an associated grade with it.
class AssignmentFeedback(Base, AssignmentSubmissionMixin, DeletedMixin):

	__tablename__ = 'AssignmentFeedback'
	feedback_ds_id = Column('feedback_ds_id', INTID_COLUMN_TYPE, nullable=True, unique=False)
	feedback_id = Column('feedback_id', Integer, Sequence('feedback_id_seq'), primary_key=True)

	feedback_length = Column('feedback_length', Integer, nullable=True)
	# Tie our feedback to our submission and grader.
	grade_id = Column('grade_id', Integer, ForeignKey("AssignmentGrades.grade_id"), nullable=False)

	_file_mime_types = relationship( 'FeedbackUserFileUploadMimeTypes', lazy="select" )

	@property
	def FileMimeTypes(self):
		result = {}
		mime_types = self._file_mime_types
		if mime_types:
			for mime_type in mime_types:
				result[mime_type.mime_type] = mime_type.count
		return result

class FeedbackUserFileUploadMimeTypes(Base, FileMimeTypeMixin):

	__tablename__ = 'FeedbackUserFileUploadMimeTypes'

	feedback_id = Column('feedback_id', Integer, ForeignKey("AssignmentFeedback.feedback_id"),
					nullable=False, index=True)

	feedback_file_upload_mime_type_id = Column(	'feedback_file_upload_mime_type_id',
											Integer,
											Sequence('feedback_file_upload_seq'),
											index=True,
					 						nullable=False,
					 						primary_key=True)

class SelfAssessmentsTaken(Base, AssignmentMixin):

	__tablename__ = 'SelfAssessmentsTaken'
	submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True, index=True, autoincrement=False)
	self_assessment_id = Column('self_assessment_id', Integer, Sequence('self_assessment_seq'),
								index=True, nullable=False, primary_key=True)

	@property
	def Submission(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.submission_id )

# SelfAssessments will not have feedback or multiple graders
class SelfAssessmentDetails(Base, BaseTableMixin, DetailMixin, GradeDetailMixin):

	__tablename__ = 'SelfAssessmentDetails'
	self_assessment_id = Column('self_assessment_id', Integer,
							ForeignKey("SelfAssessmentsTaken.self_assessment_id"),
							nullable=False, index=True)

	self_assessment_details_id = Column('self_assessment_details_id',
										Integer,
										Sequence('self_assessment_details_seq'),
										primary_key=True)

class AssignmentViewMixin(AssignmentIdMixin, ResourceMixin, BaseViewMixin, TimeLengthMixin):

	@declared_attr
	def resource_id(cls):
		return Column('resource_id', Integer,
					ForeignKey("Resources.resource_id"),
					nullable=True)

	@property
	def ResourceId(self):
		result = self._resource
		if result is not None:
			result = self._resource.resource_ds_id
		return result

class SelfAssessmentViews(Base, AssignmentViewMixin):

	__tablename__ = 'SelfAssessmentViews'
	self_assessment_view_id = Column('self_assessment_view_id',
									Integer,
									 Sequence('self_assessment_view_id_seq'),
									 primary_key=True)

class AssignmentViews(Base, AssignmentViewMixin):

	__tablename__ = 'AssignmentViews'
	assignment_view_id = Column('assignment_view_id',
								Integer,
								Sequence('assignment_view_id_seq'),
								primary_key=True)

