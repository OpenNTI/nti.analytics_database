#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy.schema import Sequence

from zope import interface

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import ResourceViewMixin

logger = __import__('logging').getLogger(__name__)


class LTIAssetLaunches(Base, ResourceViewMixin, TimeLengthMixin):

    __tablename__ = 'LTIToolLaunches'

    lti_tool_launches_id = Column('lti_tool_launch_id', Integer,
                                  Sequence('lti_tool_launch_id_seq'),
                                  primary_key=True)


from nti.analytics_database.interfaces import IDatabaseCreator
interface.moduleProvides(IDatabaseCreator)