#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.schema import Sequence

from .meta_mixins import CourseMixin
from .meta_mixins import BaseTableMixin

from . import Base
from . import NTIID_COLUMN_TYPE
from . import INTID_COLUMN_TYPE

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

	survey_id = Column('survey_id', NTIID_COLUMN_TYPE, nullable=False, index=True)
