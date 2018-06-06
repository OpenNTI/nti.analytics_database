#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy.schema import Sequence

from zope import interface, component

from nti.analytics_database import Base

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import ResourceViewMixin

logger = __import__('logging').getLogger(__name__)


class LTIAssetLaunches(Base, ResourceViewMixin, TimeLengthMixin):

    __tablename__ = 'LTIAssetLaunches'

    lti_asset_launches_id = Column('lti_asset_launch_id', Integer,
                                   Sequence('lti_asset_launch_id_seq'),
                                   primary_key=True)

    @property
    def AssetId(self):
        result = self._resource
        if result is not None:
            result = self._resource.resourse_ds_id
        return result


from nti.analytics_database.interfaces import IDatabaseCreator

interface.moduleProvides(IDatabaseCreator)
