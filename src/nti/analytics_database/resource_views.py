#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Enum
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Sequence

from nti.analytics_database import NTIID_COLUMN_TYPE

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import CreatorMixin
from nti.analytics_database.meta_mixins import BaseViewMixin
from nti.analytics_database.meta_mixins import ReferrerMixin
from nti.analytics_database.meta_mixins import ResourceMixin
from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import TimeLengthMixin
from nti.analytics_database.meta_mixins import ResourceViewMixin

from nti.property.property import alias


class CourseResourceViews(Base, ResourceViewMixin, TimeLengthMixin):

    __tablename__ = 'CourseResourceViews'

    # Need to have a seq primary key that we will not use to work around primary key limits
    # in mysql, or we could put our resource_ids into another table to conserve space (we did).
    # We'll probably just pull all of these events by indexed course; so, to avoid a join,
    # let's try this.
    resource_view_id = Column('resource_view_id', Integer,
                              Sequence('resource_view_id_seq'),
                              primary_key=True)


class VideoEvents(Base, ResourceViewMixin, TimeLengthMixin):

    __tablename__ = 'VideoEvents'

    VideoEndTime = alias('video_end_time')

    VideoStartTime = alias('video_start_time')

    WithTranscript = alias('with_transcript')

    video_event_type = Column('video_event_type',
                              Enum('WATCH', 'SKIP', validate_strings=True),
                              nullable=False)

    # seconds from beginning of video (time 0s)
    video_start_time = Column('video_start_time', Integer, nullable=False)

    video_end_time = Column('video_end_time', Integer, nullable=True)

    with_transcript = Column('with_transcript', Boolean, nullable=False)

    video_view_id = Column('video_view_id', Integer,
                           Sequence('video_view_id_seq'),
                           primary_key=True)

    play_speed = Column('play_speed', String(16), nullable=True)


class VideoPlaySpeedEvents(Base, BaseTableMixin, ResourceMixin):

    __tablename__ = 'VideoPlaySpeedEvents'

    video_play_speed_id = Column('video_play_speed_id', Integer,
                                 Sequence('video_play_speed_id_seq'),
                                 primary_key=True)

    old_play_speed = Column('old_play_speed', String(16), nullable=False)

    new_play_speed = Column('new_play_speed', String(16), nullable=False)

    video_time = Column('video_time', Integer, nullable=False)

    # Optionally link to an actual video event, if possible.
    video_view_id = Column('video_view_id', Integer, nullable=True, index=True)


class UserFileUploadViewEvents(Base, BaseViewMixin, CreatorMixin, ReferrerMixin):
    """
    Stores analytics when users view other users' uploaded files, in UGD, topics,
    or blogs.
    """

    __tablename__ = 'UserFileUploadViewEvents'

    file_view_id = Column('file_view_id', Integer,
                          Sequence('file_view_id_seq'),
                          primary_key=True)

    file_ds_id = Column('file_ds_id', NTIID_COLUMN_TYPE, nullable=True)

    file_mime_type_id = Column('file_mime_type_id', Integer,
                               ForeignKey("FileMimeTypes.file_mime_type_id"),
                               nullable=False,
                               autoincrement=False,
                               index=True)

    _file_mime_type = relationship('FileMimeTypes', lazy="select")

    @property
    def mime_type(self):
        return self._file_mime_type_id.mime_type

    @property
    def FileObject(self):
        # TODO: Register an utility
        try:
            from nti.ntiids.ntiids import find_object_with_ntiid
            return find_object_with_ntiid(self.file_ds_id)
        except ImportError:
            return None
