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

from sqlalchemy.schema import PrimaryKeyConstraint

from zope import interface

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin

logger = __import__('logging').getLogger(__name__)


class EntityProfileMixin(BaseViewMixin, TimeLengthMixin):

    @declared_attr
    def target_id(self):
        return Column('target_id', Integer, ForeignKey("Users.user_id"),
                      index=True, nullable=False)


class EntityProfileViews(Base, EntityProfileMixin):

    __tablename__ = 'EntityProfileViews'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'target_id', 'timestamp'),
    )


class EntityProfileActivityViews(Base, EntityProfileMixin):

    __tablename__ = 'EntityProfileActivityViews'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'target_id', 'timestamp'),
    )


class EntityProfileMembershipViews(Base, EntityProfileMixin):

    __tablename__ = 'EntityProfileMembershipViews'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'target_id', 'timestamp'),
    )


from nti.analytics_database.interfaces import IDatabaseCreator
interface.moduleProvides(IDatabaseCreator)
