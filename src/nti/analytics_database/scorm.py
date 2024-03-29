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

from sqlalchemy.schema import Sequence

from zope import interface

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import ResourceViewMixin

logger = __import__('logging').getLogger(__name__)


class SCORMPackageLaunches(Base, ResourceViewMixin, TimeLengthMixin):

    __tablename__ = 'SCORMPackageLaunches'

    scorm_package_launch_id = Column('scorm_package_launch_id', Integer,
                                     Sequence('scorm_package_launch_id_seq'),
                                     primary_key=True)


from nti.analytics_database.interfaces import IDatabaseCreator
interface.moduleProvides(IDatabaseCreator)
