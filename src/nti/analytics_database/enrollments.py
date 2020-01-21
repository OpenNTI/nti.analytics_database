#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint

from zope import interface

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import CourseMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin

logger = __import__('logging').getLogger(__name__)


class CourseCatalogViews(Base, BaseViewMixin, CourseMixin, TimeLengthMixin):

    __tablename__ = 'CourseCatalogViews'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'course_id', 'timestamp'),
    )


class EnrollmentTypes(Base):

    __tablename__ = 'EnrollmentTypes'

    type_id = Column('type_id', Integer, Sequence('enrollment_type_seq'),
                     nullable=False, primary_key=True)

    type_name = Column('type_name', String(64),
                       nullable=False, index=True, unique=True)


class CourseEnrollments(Base, BaseTableMixin, CourseMixin):

    __tablename__ = 'CourseEnrollments'

    type_id = Column('type_id', Integer,
                     ForeignKey('EnrollmentTypes.type_id'),
                     index=True, nullable=False)

    @declared_attr
    def _type_record(self):
        return relationship('EnrollmentTypes',
                            lazy="select",
                            foreign_keys=[self.type_id])

    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'user_id'),
    )


class CourseDrops(Base, BaseTableMixin, CourseMixin):

    __tablename__ = 'CourseDrops'

    # Make sure we allow multiple course drops, timestamp should be non-null
    # here.
    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'user_id', 'timestamp'),
    )


from nti.analytics_database.interfaces import IDatabaseCreator
interface.moduleProvides(IDatabaseCreator)
