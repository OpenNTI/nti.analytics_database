#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import CourseMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin

class CourseCatalogViews(Base, BaseViewMixin, CourseMixin, TimeLengthMixin):

	__tablename__ = 'CourseCatalogViews'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'course_id', 'timestamp'),
	)

class EnrollmentTypes(Base):

	__tablename__ = 'EnrollmentTypes'

	type_id = Column('type_id', Integer, Sequence('enrollment_type_seq'), 
					 nullable=False, primary_key=True)
	type_name = Column('type_name', String(64), nullable=False, index=True, unique=True)

class CourseEnrollments(Base, BaseTableMixin, CourseMixin):

	__tablename__ = 'CourseEnrollments'

	type_id = Column('type_id', Integer, ForeignKey('EnrollmentTypes.type_id'),
					 index=True, nullable=False)

	__table_args__ = (
		PrimaryKeyConstraint('course_id', 'user_id'),
	)

class CourseDrops(Base, BaseTableMixin, CourseMixin):

	__tablename__ = 'CourseDrops'

	# Make sure we allow multiple course drops, timestamp should be non-null here.
	__table_args__ = (
		PrimaryKeyConstraint('course_id', 'user_id', 'timestamp'),
	)
