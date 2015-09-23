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

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declared_attr

from .meta_mixins import CreatorMixin
from .meta_mixins import DeletedMixin
from .meta_mixins import RatingsMixin
from .meta_mixins import BaseViewMixin
from .meta_mixins import CommentsMixin
from .meta_mixins import BaseTableMixin
from .meta_mixins import TimeLengthMixin

from . import Base
from . import INTID_COLUMN_TYPE

class BlogMixin(object):

	@declared_attr
	def blog_id(cls):
		return Column('blog_id', Integer, ForeignKey("BlogsCreated.blog_id"), nullable=False, index=True)

class BlogsCreated(Base, BaseTableMixin, DeletedMixin, RatingsMixin):
	
	__tablename__ = 'BlogsCreated'

	blog_ds_id = Column('blog_ds_id', INTID_COLUMN_TYPE, nullable=True, autoincrement=False)
	blog_length = Column('blog_length', Integer, nullable=True, autoincrement=False)
	blog_id = Column('blog_id', Integer, Sequence('blog_seq'), index=True, nullable=False, primary_key=True)

class BlogsViewed(Base, BaseViewMixin, BlogMixin, TimeLengthMixin):

	__tablename__ = 'BlogsViewed'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'blog_id', 'timestamp'),
	)

class BlogCommentsCreated(Base, CommentsMixin, BlogMixin, RatingsMixin):
	__tablename__ = 'BlogCommentsCreated'

	__table_args__ = (
		PrimaryKeyConstraint('comment_id'),
	)

class BlogFavorites(Base, BaseTableMixin, BlogMixin, CreatorMixin):
	__tablename__ = 'BlogFavorites'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'blog_id'),
	)

class BlogLikes(Base, BaseTableMixin, BlogMixin, CreatorMixin):
	__tablename__ = 'BlogLikes'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'blog_id'),
	)

class BlogCommentMixin(object):

	@declared_attr
	def comment_id(cls):
		return Column('comment_id', 
					  INTID_COLUMN_TYPE, 
					  ForeignKey("BlogCommentsCreated.comment_id"), 
					  nullable=False, 
					  index=True)

class BlogCommentFavorites(Base, BaseTableMixin, BlogCommentMixin, CreatorMixin):

	__tablename__ = 'BlogCommentFavorites'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'comment_id'),
	)

class BlogCommentLikes(Base, BaseTableMixin, BlogCommentMixin, CreatorMixin):
	__tablename__ = 'BlogCommentLikes'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'comment_id'),
	)
