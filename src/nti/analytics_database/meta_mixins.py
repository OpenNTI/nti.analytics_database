#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import relationship

from sqlalchemy.schema import Index

from zope import component

from nti.analytics_database import INTID_COLUMN_TYPE
from nti.analytics_database import SESSION_COLUMN_TYPE
from nti.analytics_database import CONTEXT_PATH_SEPARATOR

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier
from nti.analytics_database.interfaces import IAnalyticsRootContextResolver

from nti.analytics_database.root_context import Books
from nti.analytics_database.root_context import Courses

from nti.analytics_database.users import Users

from nti.property.property import alias

logger = __import__('logging').getLogger(__name__)


class UserMixin(object):

    _user = None

    @declared_attr
    def _user_record(self):
        return relationship('Users', lazy="select", foreign_keys=[self.user_id])

    @property
    def user(self):
        result = self._user
        if result is None:
            # pylint: disable=no-member
            result = self._user_record.user
        return result

    @user.setter
    def user(self, user):
        self._user = user


class BaseTableMixin(UserMixin):

    SessionID = alias('session_id')

    # For migrating data, we may not have sessions (or timestamps); thus this
    # is optional.
    @declared_attr
    def session_id(self):
        return Column('session_id', SESSION_COLUMN_TYPE,
                      ForeignKey("Sessions.session_id"), nullable=True)

    @declared_attr
    def _session_record(self):
        return relationship('Sessions', lazy="select", foreign_keys=[self.session_id])

    @declared_attr
    def user_id(self):
        return Column('user_id', Integer, ForeignKey("Users.user_id"),
                      index=True, nullable=True)

    timestamp = Column('timestamp', DateTime, nullable=True, index=True)


class BaseViewMixin(UserMixin):

    SessionID = alias('session_id')

    # For resource views, we need timestamp to be non-null for primary key purposes.
    # It will have to be fine-grain to avoid collisions.
    @declared_attr
    def session_id(self):
        return Column('session_id', SESSION_COLUMN_TYPE,
                      ForeignKey("Sessions.session_id"), nullable=True)

    @declared_attr
    def user_id(self):
        return Column('user_id', Integer, ForeignKey("Users.user_id"), index=True)

    timestamp = Column('timestamp', DateTime, index=True)

    # Dashboard/lesson_ntiid
    context_path = Column('context_path', String(1048), nullable=True)

    @property
    def ContextPath(self):
        result = self.context_path
        if result:
            result = result.split(CONTEXT_PATH_SEPARATOR)
        return result


class DeletedMixin(object):

    deleted = Column('deleted', DateTime)


class ReferrerMixin(object):

    referrer = Column('referrer', String(1024), nullable=True, index=False)


class CourseMixin(object):

    @declared_attr
    def course_id(self):
        return Column('course_id', Integer,
                       ForeignKey("Courses.context_id"),
                       nullable=False, index=True,
                       autoincrement=False)

    @declared_attr
    def _course_record(self):
        return relationship('Courses', lazy="select", foreign_keys=[self.course_id])

    @declared_attr
    def __table_args__(self):
        return (Index('ix_%s_user_course' % self.__tablename__, 'user_id', 'course_id'),)

    _root_context_record = alias('_course_record')


class RootContextMixin(object):

    _RootContext = None

    entity_root_context_id = Column('entity_root_context_id', Integer,
                                    nullable=True, index=True, autoincrement=False)

    # TODO: Rename this column for relevant tables.
    root_context_id = Column('course_id', Integer, nullable=True, index=True,
                             autoincrement=False)

    @declared_attr
    def _book_context_record(self):
        return relationship('Books', lazy="select", foreign_keys=[self.root_context_id],
                            primaryjoin=lambda: Books.context_id == self.root_context_id)

    @declared_attr
    def _course_context_record(self):
        return relationship('Courses', lazy="select", foreign_keys=[self.root_context_id],
                            primaryjoin=lambda: Courses.context_id == self.root_context_id)

    @property
    def RootContext(self):
        result = self._RootContext
        if result is None:
            resolver = component.queryUtility(IAnalyticsRootContextResolver)
            result = resolver(self) if resolver is not None else None
        return result

    @RootContext.setter
    def RootContext(self, root_context):
        self._RootContext = root_context

    @declared_attr
    def _entity_root_context_record(self):
        return relationship('Users', lazy="select", foreign_keys=[self.entity_root_context_id],
                            primaryjoin=lambda: Users.user_id == self.entity_root_context_id)

    @property
    def _root_context_record(self):
        return self._book_context_record or self._course_context_record

    @_root_context_record.setter
    def _root_context_record(self, value):
        if not value:
            return
        if value.__tablename__ == 'Books':
            self._book_context_record = value
        else:
            self._course_context_record = value

    # BWC
    course_id = alias('root_context_id')


class ResourceMixin(RootContextMixin):

    _MaxDuration = None

    @declared_attr
    def _resource(self):
        return relationship('Resources', lazy="select", foreign_keys=[self.resource_id])

    @declared_attr
    def resource_id(self):
        return Column('resource_id', Integer, ForeignKey("Resources.resource_id"),
                      nullable=False, index=True)

    @property
    def ResourceId(self):
        # pylint: disable=no-member
        return self._resource.resource_ds_id

    @property
    def MaxDuration(self):
        # pylint: disable=no-member
        return self._MaxDuration or self._resource.max_time_length

    @MaxDuration.setter
    def MaxDuration(self, max_duration):
        self._MaxDuration = max_duration

    @property
    def Title(self):
        # pylint: disable=no-member
        return self._resource.resource_display_name


class ResourceViewMixin(ResourceMixin, BaseViewMixin):
    pass


class FavoriteMixin(object):

    FavoriteCount = alias('favorite_count')

    favorite_count = Column('favorite_count', Integer, nullable=True)


class RatingsMixin(FavoriteMixin):

    Flagged = alias('is_flagged')
    LikeCount = alias('like_count')

    is_flagged = Column('is_flagged', Boolean, nullable=True)

    like_count = Column('like_count', Integer, nullable=True)


class CreatorMixin(object):
    """
    For tables referencing an object with a creator.
    """
    _creator = None

    @declared_attr
    def creator_id(self):
        return Column('creator_id', Integer, ForeignKey("Users.user_id"), index=True)

    @declared_attr
    def _creator_record(self):
        return relationship('Users', lazy="select", foreign_keys=[self.creator_id])

    @property
    def ObjectCreator(self):
        result = self._creator
        if self._creator is None:
            # pylint: disable=no-member
            result = self._creator_record.user
        return result

    @ObjectCreator.setter
    def ObjectCreator(self, creator):
        self._creator = creator


class TimeLengthMixin(object):
    """
    A mixin that captures time_length/Duration in seconds.
    """

    Duration = alias('time_length')

    time_length = Column('time_length', Integer, nullable=True)


class ReplyToMixin(object):

    _replied_to_user = None

    # parent_id should point to a parent comment; top-level comments will have
    # null parent_ids
    @declared_attr
    def parent_id(self):
        return Column('parent_id', INTID_COLUMN_TYPE)

    @declared_attr
    def _parent_user_record(self):
        return relationship('Users', lazy="select",
                            foreign_keys=[self.parent_user_id])

    @declared_attr
    def parent_user_id(self):
        return Column('parent_user_id', Integer,
                      ForeignKey("Users.user_id"), index=True, nullable=True)

    @property
    def IsReply(self):
        return bool(self.parent_id is not None)

    @property
    def RepliedToUser(self):
        result = self._replied_to_user
        if result is None and self._parent_user_record:
            # pylint: disable=no-member
            result = self._parent_user_record.user
        return result

    @RepliedToUser.setter
    def RepliedToUser(self, replied_to_user):
        self._replied_to_user = replied_to_user


class CommentsMixin(BaseTableMixin, DeletedMixin, ReplyToMixin):

    CommentLength = alias('comment_length')

    # comment_id should be the DS intid
    @declared_attr
    def comment_id(self):
        return Column('comment_id', INTID_COLUMN_TYPE, index=True,
                      nullable=False, autoincrement=False)

    @declared_attr
    def comment_length(self):
        return Column('comment_length', Integer, nullable=True, autoincrement=False)

    @property
    def Comment(self):
        id_util = component.queryUtility(IAnalyticsIntidIdentifier)
        return id_util.get_object(self.comment_id) if id_util is not None else None


class FileMimeTypeMixin(object):

    Count = alias('count')
    MimeType = alias('mime_type')

    @declared_attr
    def count(self):
        return Column('count', Integer, index=False, nullable=False,
                      autoincrement=False)

    @declared_attr
    def file_mime_type_id(self):
        return Column('file_mime_type_id', Integer,
                      ForeignKey("FileMimeTypes.file_mime_type_id"),
                      nullable=False,
                      autoincrement=False,
                      index=True)

    @declared_attr
    def _mime_type(self):
        return relationship('FileMimeTypes', lazy="select", foreign_keys=[self.file_mime_type_id])

    @property
    def mime_type(self):
        # pylint: disable=no-member
        return self._mime_type.mime_type
