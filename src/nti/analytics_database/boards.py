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

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declared_attr

from zope import component

from .interfaces import IAnalyticsIntidIdentifier

from .meta_mixins import CreatorMixin
from .meta_mixins import DeletedMixin
from .meta_mixins import RatingsMixin
from .meta_mixins import BaseViewMixin
from .meta_mixins import CommentsMixin
from .meta_mixins import BaseTableMixin
from .meta_mixins import TimeLengthMixin
from .meta_mixins import RootContextMixin

from . import Base
from . import INTID_COLUMN_TYPE

class ForumMixin(RootContextMixin):

	_forum = None

	@declared_attr
	def forum_id(cls):
		return Column('forum_id', Integer, ForeignKey("ForumsCreated.forum_id"), nullable=False, index=True)

	@declared_attr
	def _forum_record(self):
		return relationship( 'ForumsCreated', lazy="select" )

	@property
	def Forum(self):
		result = self._forum
		if result is None:
			result = self._forum_record.Forum
		return result

	@Forum.setter
	def Forum(self, forum):
		self._forum = forum

class TopicMixin(ForumMixin):

	_topic = None

	@declared_attr
	def topic_id(cls):
		return Column('topic_id', Integer, ForeignKey("TopicsCreated.topic_id"), nullable=False, index=True)

	@declared_attr
	def _topic_record(self):
		return relationship( 'TopicsCreated', lazy="select" )

	@property
	def Topic(self):
		result = self._topic
		if result is None:
			result = self._topic_record.Topic
		return result

	@Topic.setter
	def Topic(self, topic):
		self._topic = topic

class ForumsCreated(Base, BaseTableMixin, RootContextMixin, DeletedMixin):

	__tablename__ = 'ForumsCreated'

	forum_ds_id = Column('forum_ds_id', INTID_COLUMN_TYPE, nullable=True, index=True, autoincrement=False)
	forum_id = Column('forum_id', Integer, Sequence('forum_seq'), index=True, nullable=False, primary_key=True)

	@property
	def Forum(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.forum_ds_id )

class TopicsCreated(Base, BaseTableMixin, ForumMixin, DeletedMixin, RatingsMixin):

	__tablename__ = 'TopicsCreated'

	topic_ds_id = Column('topic_ds_id', INTID_COLUMN_TYPE, nullable=True, autoincrement=False, index=True)
	topic_id = Column('topic_id', Integer, Sequence('topic_seq'), index=True, nullable=False, primary_key=True)

	@property
	def Topic(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.topic_ds_id )

class ForumCommentsCreated(Base, CommentsMixin, TopicMixin, RatingsMixin):

	__tablename__ = 'ForumCommentsCreated'

	__table_args__ = (
		PrimaryKeyConstraint('comment_id'),
	)

class TopicsViewed(Base, BaseViewMixin, TopicMixin, TimeLengthMixin):

	__tablename__ = 'TopicsViewed'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'topic_id', 'timestamp'),
	)

class TopicRatingMixin(BaseTableMixin, CreatorMixin, RootContextMixin):

	@declared_attr
	def topic_id(cls):
		return Column('topic_id', Integer, ForeignKey("TopicsCreated.topic_id"), nullable=False, index=True)

class TopicFavorites(Base, TopicRatingMixin):

	__tablename__ = 'TopicFavorites'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'topic_id'),
	)

class TopicLikes(Base, TopicRatingMixin):

	__tablename__ = 'TopicLikes'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'topic_id'),
	)

class ForumCommentMixin(object):

	@declared_attr
	def comment_id(cls):
		return Column('comment_id',
					  INTID_COLUMN_TYPE,
					  ForeignKey("ForumCommentsCreated.comment_id"),
					  nullable=False,
					  index=True)

class ForumCommentFavorites(Base, BaseTableMixin, ForumCommentMixin, CreatorMixin, RootContextMixin):

	__tablename__ = 'ForumCommentFavorites'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'comment_id'),
	)

class ForumCommentLikes(Base, BaseTableMixin, ForumCommentMixin, CreatorMixin, RootContextMixin):

	__tablename__ = 'ForumCommentLikes'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'comment_id'),
	)
