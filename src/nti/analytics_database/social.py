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

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint

from zope import component

from nti.analytics_database import Base
from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.meta_mixins import DeletedMixin
from nti.analytics_database.meta_mixins import BaseTableMixin

from nti.property.property import alias

class DynamicFriendsListMixin(object):

	@declared_attr
	def dfl_id(cls):
		return Column('dfl_id', Integer, ForeignKey("DynamicFriendsListsCreated.dfl_id"), nullable=False, index=True)

class FriendMixin(object):

	@declared_attr
	def target_id(cls):
		return Column('target_id', Integer, ForeignKey("Users.user_id"), index=True)

	@declared_attr
	def _target_record(self):
		return relationship( 'Users', lazy="select", foreign_keys=[self.target_id] )

	@property
	def _target_entity(self):
		return self._target_record.user

class FriendsListMixin(object):

	@declared_attr
	def friends_list_id(cls):
		return Column('friends_list_id', Integer, ForeignKey("FriendsListsCreated.friends_list_id"), nullable=False, index=True)

# This information needs to be obscured to protect privacy.
class ChatsInitiated(Base, BaseTableMixin):

	__tablename__ = 'ChatsInitiated'

	chat_ds_id = Column('chat_ds_id', INTID_COLUMN_TYPE, index=True, nullable=True, autoincrement=False)
	chat_id = Column('chat_id', Integer, Sequence('chat_seq'), index=True, nullable=False, primary_key=True)

# Note, we're not tracking when users leave chat rooms.
class ChatsJoined(Base, BaseTableMixin):

	__tablename__ = 'ChatsJoined'

	chat_id = Column('chat_id', Integer, ForeignKey("ChatsInitiated.chat_id"), nullable=False, index=True)

	__table_args__ = (
		PrimaryKeyConstraint('chat_id', 'user_id', 'timestamp'),
	)

class DynamicFriendsListsCreated(Base, BaseTableMixin, DeletedMixin):

	__tablename__ = 'DynamicFriendsListsCreated'

	dfl_ds_id = Column('dfl_ds_id', INTID_COLUMN_TYPE, index=True, nullable=True, autoincrement=False)
	dfl_id = Column('dfl_id', Integer, Sequence('dfl_seq'), index=True, nullable=False, primary_key=True)

	@property
	def Group(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.dfl_ds_id )

class DynamicFriendsListsMemberAdded(Base, BaseTableMixin, DynamicFriendsListMixin, FriendMixin):

	__tablename__ = 'DynamicFriendsListsMemberAdded'

	__table_args__ = (
		PrimaryKeyConstraint('dfl_id', 'target_id'),
	)

class DynamicFriendsListsMemberRemoved(Base, BaseTableMixin, DynamicFriendsListMixin, FriendMixin):

	__tablename__ = 'DynamicFriendsListsMemberRemoved'

	# Make sure we allow multiple removals
	__table_args__ = (
		PrimaryKeyConstraint('dfl_id', 'target_id', 'timestamp'),
	)

class FriendsListsCreated(Base, BaseTableMixin, DeletedMixin):

	__tablename__ = 'FriendsListsCreated'

	friends_list_ds_id = Column('friends_list_ds_id', INTID_COLUMN_TYPE, index=True, nullable=True, autoincrement=False)
	friends_list_id = Column('friends_list_id', Integer, Sequence('friends_list_seq'), index=True, nullable=False, primary_key=True)

class FriendsListsMemberAdded(Base, BaseTableMixin, FriendsListMixin, FriendMixin):

	__tablename__ = 'FriendsListsMemberAdded'

	__table_args__ = (
		PrimaryKeyConstraint('friends_list_id', 'target_id'),
	)

class FriendsListsMemberRemoved(Base, BaseTableMixin, FriendsListMixin, FriendMixin):

	__tablename__ = 'FriendsListsMemberRemoved'

	# Make sure we allow multiple removals
	__table_args__ = (
		PrimaryKeyConstraint('friends_list_id', 'target_id', 'timestamp'),
	)

class ContactsAdded(Base, BaseTableMixin, FriendMixin):

	__tablename__ = 'ContactsAdded'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'target_id'),
	)

	Contact = alias( '_target_entity' )

class ContactsRemoved(Base, BaseTableMixin, FriendMixin):

	__tablename__ = 'ContactsRemoved'

	# Make sure we allow multiple contact drops
	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'target_id', 'timestamp'),
	)
