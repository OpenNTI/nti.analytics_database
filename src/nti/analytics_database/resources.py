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

from sqlalchemy.schema import Sequence

from nti.analytics_database import Base
from nti.analytics_database import NTIID_COLUMN_TYPE

class Resources(Base):

	__tablename__ = 'Resources'

	resource_id = Column('resource_id', Integer, Sequence('resource_id_seq'), 
						 index=True, nullable=False, primary_key=True)
	resource_ds_id = Column('resource_ds_id', NTIID_COLUMN_TYPE, index=True, 
							nullable=False)
	resource_display_name = Column('resource_display_name', String(128), 
								   unique=False, nullable=True)
	# Only applicable for videos
	max_time_length = Column('max_time_length', Integer, nullable=True)
