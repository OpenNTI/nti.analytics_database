#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy.schema import Sequence

from . import Base
from . import INTID_COLUMN_TYPE

class Users(Base):

	__tablename__ = 'Users'

	user_id = Column('user_id', Integer, Sequence('user_id_seq'), index=True, nullable=False, primary_key=True)
	user_ds_id = Column('user_ds_id', INTID_COLUMN_TYPE, nullable=True, index=True)
	allow_research = Column('allow_research', Boolean, nullable=True, default=None)
	username = Column('username', String(64), nullable=True, unique=False, index=True)
	username2 = Column('username2', String(64), nullable=True, unique=False)
	create_date = Column('create_date', DateTime, nullable=True)
