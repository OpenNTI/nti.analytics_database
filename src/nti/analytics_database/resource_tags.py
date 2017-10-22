#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy import Enum
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence
from sqlalchemy.schema import PrimaryKeyConstraint

from zope import component

from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database import Base

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier

from nti.analytics_database.meta_mixins import CreatorMixin
from nti.analytics_database.meta_mixins import DeletedMixin
from nti.analytics_database.meta_mixins import RatingsMixin
from nti.analytics_database.meta_mixins import ReplyToMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import ResourceMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import RootContextMixin
from nti.analytics_database.meta_mixins import FileMimeTypeMixin

from nti.property.property import alias

SHARING_ENUMS = Enum(u'GLOBAL', u'PRIVATE_COURSE', u'PUBLIC_COURSE',
                     u'PRIVATE', u'OTHER', validate_strings=True)

logger = __import__('logging').getLogger(__name__)


class NoteMixin(ResourceMixin):

    _note = None

    @declared_attr
    def note_id(self):
        return Column('note_id', Integer, ForeignKey("NotesCreated.note_id"),
                      nullable=False, index=True)

    @declared_attr
    def _note_record(self):
        return relationship('NotesCreated', lazy="select",
                            foreign_keys=[self.note_id])

    @property
    def Note(self):
        result = self._note
        if result is None:
            result = self._note_record.Note
        return result

    @Note.setter
    def Note(self, note):
        self._note = note


class NotesCreated(Base, BaseTableMixin, ResourceMixin, DeletedMixin,
                   RatingsMixin, ReplyToMixin):

    __tablename__ = 'NotesCreated'

    Sharing = alias('sharing')
    NoteLength = alias('note_length')

    note_ds_id = Column('note_ds_id', INTID_COLUMN_TYPE, index=True,
                        nullable=True, unique=False, autoincrement=False)

    note_id = Column('note_id', Integer, Sequence('note_seq'), index=True,
                     nullable=False, primary_key=True)

    # Parent-id should be other notes; top-level notes will have null
    # parent_ids
    sharing = Column('sharing', SHARING_ENUMS, nullable=False)

    note_length = Column('note_length', Integer, nullable=True)

    @property
    def Note(self):
        id_utility = component.getUtility(IAnalyticsIntidIdentifier)
        return id_utility.get_object(self.note_ds_id)

    _file_mime_types = relationship('NotesUserFileUploadMimeTypes',
                                    lazy="select")

    @property
    def FileMimeTypes(self):
        result = {}
        for mime_type in self._file_mime_types or ():
            result[mime_type.mime_type] = mime_type.count
        return result


class NotesUserFileUploadMimeTypes(Base, FileMimeTypeMixin):

    __tablename__ = 'NotesUserFileUploadMimeTypes'

    note_id = Column('note_id', Integer, ForeignKey("NotesCreated.note_id"),
                     nullable=False, index=True)

    note_file_upload_mime_type_id = Column(	'note_file_upload_mime_type_id',
                                            Integer,
                                            Sequence('note_file_upload_seq'),
                                            index=True,
                                            nullable=False,
                                            primary_key=True)


class NotesViewed(Base, BaseViewMixin, NoteMixin):

    __tablename__ = 'NotesViewed'

    __table_args__ = (
        PrimaryKeyConstraint('note_id', 'user_id', 'timestamp'),
    )


class NoteRatingMixin(CreatorMixin, RootContextMixin):

    @declared_attr
    def note_id(self):
        return Column('note_id', Integer, ForeignKey("NotesCreated.note_id"),
                      nullable=False, index=True)


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

    @property
    def Highlight(self):
        id_utility = component.getUtility(IAnalyticsIntidIdentifier)
        return id_utility.get_object(self.highlight_ds_id)


class BookmarksCreated(Base, BaseTableMixin, ResourceMixin, DeletedMixin):
    """
    Store bookmarks on content objects.
    """
    __tablename__ = 'BookmarksCreated'

    bookmark_ds_id = Column('bookmark_ds_id', INTID_COLUMN_TYPE, index=True,
                            nullable=True, autoincrement=False)

    bookmark_id = Column('bookmark_id', Integer, Sequence('bookmark_seq'), index=True,
                         nullable=False, primary_key=True)

    @property
    def Bookmark(self):
        id_utility = component.getUtility(IAnalyticsIntidIdentifier)
        return id_utility.get_object(self.bookmark_ds_id)
