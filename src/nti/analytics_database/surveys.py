#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.schema import Sequence

from nti.analytics_database import Base
from nti.analytics_database import NTIID_COLUMN_TYPE
from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database.meta_mixins import CourseMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import ResourceMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin

from nti.property.property import alias

logger = __import__('logging').getLogger(__name__)


class InquiryMixin(BaseTableMixin, CourseMixin):
    pass


class SurveyIdMixin(object):

    AssessmentId = SurveyId = alias('survey_id')

    @declared_attr
    def survey_id(self):
        return Column('survey_id', NTIID_COLUMN_TYPE,
                      nullable=False, index=True)


class PollsTaken(Base, InquiryMixin):

    __tablename__ = 'PollsTaken'

    submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True,
                           index=True, autoincrement=False)

    poll_taken_id = Column('poll_taken_id', Integer, Sequence('poll_taken_seq'),
                           index=True, nullable=False, primary_key=True)

    poll_id = Column('poll_id', NTIID_COLUMN_TYPE, nullable=False, index=True)


class SurveysTaken(Base, SurveyIdMixin, InquiryMixin):

    __tablename__ = 'SurveysTaken'

    submission_id = Column('submission_id', INTID_COLUMN_TYPE, nullable=True,
                           index=True, autoincrement=False)

    survey_taken_id = Column('survey_taken_id', Integer, Sequence('survey_taken_seq'),
                             index=True, nullable=False, primary_key=True)


class SurveyViews(Base, SurveyIdMixin, ResourceMixin, BaseViewMixin, TimeLengthMixin):

    __tablename__ = 'SurveyViews'

    survey_view_id = Column('survey_view_id',
                            Integer,
                            Sequence('survey_view_id_seq'),
                            primary_key=True)

    resource_id = Column('resource_id', Integer,
                         ForeignKey("Resources.resource_id"),
                         nullable=True)

    @property
    def ResourceId(self):
        result = self._resource
        if result is not None:
            # pylint: disable=no-member
            result = self._resource.resource_ds_id
        return result

