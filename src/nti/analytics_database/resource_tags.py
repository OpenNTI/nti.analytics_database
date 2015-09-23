#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Enum
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declared_attr

from .meta_mixins import CreatorMixin
from .meta_mixins import RatingsMixin
from .meta_mixins import DeletedMixin
from .meta_mixins import BaseViewMixin
from .meta_mixins import ResourceMixin
from .meta_mixins import BaseTableMixin
from .meta_mixins import RootContextMixin

from . import Base
from . import INTID_COLUMN_TYPE

class NoteMixin(ResourceMixin):

	@declared_attr
	def note_id(cls):
		return Column('note_id', Integer, ForeignKey("NotesCreated.note_id"), nullable=False, index=True)

class NotesCreated(Base, BaseTableMixin, ResourceMixin, DeletedMixin, RatingsMixin):
	
	__tablename__ = 'NotesCreated'
	
	note_ds_id = Column('note_ds_id', INTID_COLUMN_TYPE, index=True, nullable=True,
						unique=False, autoincrement=False)
	
	note_id = Column('note_id', Integer, Sequence('note_seq'), index=True,
					 nullable=False, primary_key=True)

	# Parent-id should be other notes; top-level notes will have null parent_ids
	parent_id = Column('parent_id', Integer, nullable=True)
	parent_user_id = Column('parent_user_id', Integer, index=True, nullable=True)
	sharing = Column('sharing', Enum('PUBLIC', 'COURSE', 'OTHER', 'UNKNOWN'),
					 nullable=False)
	note_length = Column('note_length', Integer, nullable=True)

class NotesViewed(Base, BaseViewMixin, NoteMixin):

	__tablename__ = 'NotesViewed'

	__table_args__ = (
		PrimaryKeyConstraint('note_id', 'user_id', 'timestamp'),
	)

class NoteRatingMixin(CreatorMixin, RootContextMixin):

	@declared_attr
	def note_id(cls):
		return Column('note_id', Integer, ForeignKey("NotesCreated.note_id"), nullable=False, index=True)

class NoteFavorites(Base, BaseTableMixin, NoteRatingMixin):

	__tablename__ = 'NoteFavorites'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'note_id'),
	)

class NoteLikes(Base, BaseTableMixin, NoteRatingMixin):

	__tablename__ = 'NoteLikes'

	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'note_id'),
	)

class HighlightsCreated(Base, BaseTableMixin, ResourceMixin, DeletedMixin):

	__tablename__ = 'HighlightsCreated'

	highlight_ds_id = Column('highlight_ds_id', INTID_COLUMN_TYPE, index=True,
							 nullable=True, autoincrement=False)

	highlight_id = Column('highlight_id', Integer, Sequence('highlight_seq'), index=True,
						  nullable=False, primary_key=True)

class BookmarksCreated(Base, BaseTableMixin, ResourceMixin, DeletedMixin):
	"""
	Store bookmarks on content objects.
	"""
	__tablename__ = 'BookmarksCreated'

	bookmark_ds_id = Column('bookmark_ds_id', INTID_COLUMN_TYPE, index=True,
							nullable=True, autoincrement=False)

	bookmark_id = Column('bookmark_id', Integer, Sequence('bookmark_seq'), index=True,
						 nullable=False, primary_key=True)
