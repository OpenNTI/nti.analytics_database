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
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean

from sqlalchemy.schema import Sequence

from .meta_mixins import ResourceMixin
from .meta_mixins import BaseTableMixin
from .meta_mixins import TimeLengthMixin
from .meta_mixins import ResourceViewMixin

from . import Base

class CourseResourceViews(Base, ResourceViewMixin, TimeLengthMixin):

	__tablename__ = 'CourseResourceViews'

	# Need to have a seq primary key that we will not use to work around primary key limits
	# in mysql, or we could put our resource_ids into another table to conserve space (we did).
	# We'll probably just pull all of these events by indexed course; so, to avoid a join,
	# let's try this.
	resource_view_id = Column('resource_view_id', Integer, Sequence('resource_view_id_seq'), primary_key=True)

class VideoEvents(Base, ResourceViewMixin, TimeLengthMixin):

	__tablename__ = 'VideoEvents'

	video_event_type = Column('video_event_type', Enum('WATCH', 'SKIP'), nullable=False)
	# seconds from beginning of video (time 0s)
	video_start_time = Column('video_start_time', Integer, nullable=False)
	video_end_time = Column('video_end_time', Integer, nullable=True)
	with_transcript = Column('with_transcript', Boolean, nullable=False)
	video_view_id = Column('video_view_id', Integer, Sequence('video_view_id_seq'), primary_key=True)
	play_speed = Column('play_speed', String(16), nullable=True)

class VideoPlaySpeedEvents(Base, BaseTableMixin, ResourceMixin):

	__tablename__ = 'VideoPlaySpeedEvents'

	video_play_speed_id = Column('video_play_speed_id', Integer,
								 Sequence('video_play_speed_id_seq'), primary_key=True)
	old_play_speed = Column('old_play_speed', String(16), nullable=False)
	new_play_speed = Column('new_play_speed', String(16), nullable=False)
	video_time = Column('video_time', Integer, nullable=False)

	# Optionally link to an actual video event, if possible.
	video_view_id = Column('video_view_id', Integer, nullable=True, index=True)
