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
from sqlalchemy import ForeignKey

from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declared_attr

from .meta_mixins import BaseViewMixin
from .meta_mixins import TimeLengthMixin

from . import Base

class EntityProfileMixin(BaseViewMixin, TimeLengthMixin):

	@declared_attr
	def target_id(cls):
		return Column('target_id', Integer, ForeignKey("Users.user_id"), index=True, nullable=False)

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
