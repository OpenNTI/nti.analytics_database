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
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Interval

from sqlalchemy.schema import Sequence

from . import Base
from . import NTIID_COLUMN_TYPE

class RootContext(object):
	"""
	Stores root context objects of other events, such as courses and books.
	"""
	context_id = Column('context_id', Integer, index=True, nullable=False, primary_key=True, autoincrement=False)
	context_ds_id = Column('context_ds_id', NTIID_COLUMN_TYPE, nullable=True, index=True)
	context_name = Column('context_name', String(64), nullable=True, unique=False, index=True)
	context_long_name = Column('context_long_name', NTIID_COLUMN_TYPE, nullable=True)
	start_date = Column('start_date', DateTime, nullable=True)
	end_date = Column('end_date', DateTime, nullable=True)
	# This interval may be represented as time since epoch (e.g. mysql)
	duration = Column('duration', Interval, nullable=True)

class Courses(Base, RootContext):

	__tablename__ = 'Courses'

	term = Column('term', String(32), nullable=True, unique=False)
	crn = Column('crn', String(32), nullable=True, unique=False)

class Books(Base, RootContext):
	__tablename__ = 'Books'

class _RootContextId(Base):
	"""
	A table to share a sequence between our RootContext tables; needed in mysql.
	"""
	
	__tablename__ = 'ContextId'
	
	# Start at 100 for simple migration.
	context_id = Column('context_id', Integer, Sequence('context_id_seq', start=1000),
						nullable=False, primary_key=True)
