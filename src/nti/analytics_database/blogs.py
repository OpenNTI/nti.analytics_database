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

from nti.common.property import alias

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.meta_mixins import CreatorMixin
from nti.analytics_database.meta_mixins import DeletedMixin
from nti.analytics_database.meta_mixins import RatingsMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import CommentsMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import FileMimeTypeMixin

from nti.analytics_database import Base
from nti.analytics_database import INTID_COLUMN_TYPE

class BlogMixin(object):

	@declared_attr
	def blog_id(cls):
		return Column('blog_id', Integer, ForeignKey("BlogsCreated.blog_id"), nullable=False, index=True)

	@declared_attr
	def _blog_record(self):
		return relationship( 'BlogsCreated', lazy="select", foreign_keys=[self.blog_id] )

	@property
	def Blog(self):
		return self._blog_record.Blog

class BlogsCreated(Base, BaseTableMixin, DeletedMixin, RatingsMixin):

	__tablename__ = 'BlogsCreated'

	BlogLength = alias( 'blog_length' )

	blog_ds_id = Column('blog_ds_id', INTID_COLUMN_TYPE, nullable=True, autoincrement=False)
	blog_length = Column('blog_length', Integer, nullable=True, autoincrement=False)
	blog_id = Column('blog_id', Integer, Sequence('blog_seq'), index=True, nullable=False, primary_key=True)

	@property
	def Blog(self):
		id_utility = component.getUtility( IAnalyticsIntidIdentifier )
		return id_utility.get_object( self.blog_ds_id )

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

	_file_mime_types = relationship( 'BlogCommentsUserFileUploadMimeTypes', lazy="select" )

	@property
	def FileMimeTypes(self):
		result = {}
		mime_types = self._file_mime_types
		if mime_types:
			for mime_type in mime_types:
				result[mime_type.mime_type] = mime_type.count
		return result

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

class BlogCommentsUserFileUploadMimeTypes(Base, FileMimeTypeMixin, BlogCommentMixin):

	__tablename__ = 'BlogCommentsUserFileUploadMimeTypes'

	blog_comment_file_upload_mime_type_id = Column('blog_comment_file_upload_mime_type_id',
											Integer,
											Sequence('blog_comment_file_upload_seq'),
											index=True,
					 						nullable=False,
					 						primary_key=True)

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
