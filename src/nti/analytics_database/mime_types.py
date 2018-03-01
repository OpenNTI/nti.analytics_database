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
from sqlalchemy import Integer

from sqlalchemy.schema import Sequence

from zope import interface

from nti.analytics_database import Base

logger = __import__('logging').getLogger(__name__)


class FileMimeTypes(Base):

    __tablename__ = 'FileMimeTypes'

    file_mime_type_id = Column('file_mime_type_id', Integer,
                               Sequence('file_mime_type_id_seq'),
                               primary_key=True)

    mime_type = Column('mime_type', String(128), nullable=False, index=True)


from nti.analytics_database.interfaces import IDatabaseCreator
interface.moduleProvides(IDatabaseCreator)
