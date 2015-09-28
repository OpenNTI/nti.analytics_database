#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.schema import Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .meta_mixins import CourseMixin
from .meta_mixins import DeletedMixin
from .meta_mixins import BaseViewMixin
from .meta_mixins import BaseTableMixin
from .meta_mixins import TimeLengthMixin
from .meta_mixins import RootContextMixin

from . import Base
from . import NTIID_COLUMN_TYPE
from . import INTID_COLUMN_TYPE

class AssignmentIdMixin(object):

	@declared_attr
	def assignment_id(cls):
		return Column('assignment_id', NTIID_COLUMN_TYPE, nullable=False, index=True)

class AssignmentMixin(BaseTableMixin, CourseMixin, TimeLengthMixin, AssignmentIdMixin):
	pass

class AssignmentsTaken(Base, AssignmentMixin):
	__tablename__ = 'AssignmentsTaken'
	submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True, index=True, autoincrement=False)

	assignment_taken_id = Column('assignment_taken_id', Integer, Sequence('assignments_taken_seq'),
								index=True, nullable=False, primary_key=True)

	# We may have multiple grades in the future.
	grade = relationship('AssignmentGrades', uselist=False, lazy='joined')

	is_late = Column('is_late', Boolean, nullable=True)

class AssignmentSubmissionMixin(BaseTableMixin):

	@declared_attr
	def assignment_taken_id(cls):
		return Column('assignment_taken_id',
					  Integer,
					  ForeignKey("AssignmentsTaken.assignment_taken_id"),
					  nullable=False, 
					  index=True)

class DetailMixin(TimeLengthMixin):

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

class GradeMixin(object):

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

class GradeDetailMixin(GradeMixin):

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

class SelfAssessmentsTaken(Base, AssignmentMixin):

	__tablename__ = 'SelfAssessmentsTaken'
	submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True, index=True, autoincrement=False)
	self_assessment_id = Column('self_assessment_id', Integer, Sequence('self_assessment_seq'),
								index=True, nullable=False, primary_key=True)

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

class AssignmentViewMixin(AssignmentIdMixin, RootContextMixin, BaseViewMixin, TimeLengthMixin):

	@declared_attr
	def resource_id(cls):
		return Column('resource_id', Integer, nullable=True)

class SelfAssessmentViews(Base, AssignmentViewMixin):

	__tablename__ = 'SelfAssessmentViews'
	self_assessment_view_id = Column('self_assessment_view_id', Integer,
									 Sequence('self_assessment_view_id_seq'), primary_key=True)

class AssignmentViews(Base, AssignmentViewMixin):

	__tablename__ = 'AssignmentViews'
	assignment_view_id = Column('assignment_view_id', 
								Integer,
								Sequence('assignment_view_id_seq'),
								primary_key=True)

