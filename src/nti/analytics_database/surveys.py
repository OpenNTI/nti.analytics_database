#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy.schema import Sequence

from nti.analytics_database import Base
from nti.analytics_database import NTIID_COLUMN_TYPE
from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database.meta_mixins import CourseMixin
from nti.analytics_database.meta_mixins import BaseTableMixin


class InquiryMixin(BaseTableMixin, CourseMixin):
    pass


class PollsTaken(Base, InquiryMixin):

    __tablename__ = 'PollsTaken'

    submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True,
                           index=True, autoincrement=False)

    poll_taken_id = Column('poll_taken_id', Integer, Sequence('poll_taken_seq'),
                           index=True, nullable=False, primary_key=True)

    poll_id = Column('poll_id', NTIID_COLUMN_TYPE, nullable=False, index=True)


class SurveysTaken(Base, InquiryMixin):

    __tablename__ = 'SurveysTaken'

    submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True,
                           index=True, autoincrement=False)

    survey_taken_id = Column('survey_taken_id', Integer, Sequence('survey_taken_seq'),
                             index=True, nullable=False, primary_key=True)

    survey_id = Column('survey_id', NTIID_COLUMN_TYPE,
                       nullable=False, index=True)
