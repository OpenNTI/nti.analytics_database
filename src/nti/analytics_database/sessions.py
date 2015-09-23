#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.schema import Sequence

from . import Base
from . import SESSION_COLUMN_TYPE

class Sessions(Base):

	__tablename__ = 'Sessions'

	session_id = Column('session_id', SESSION_COLUMN_TYPE, Sequence('session_id_seq'), index=True, primary_key=True)
	user_id = Column('user_id', Integer, ForeignKey("Users.user_id"), index=True, nullable=False)
	ip_addr = Column('ip_addr', String(64))
	user_agent_id = Column('user_agent_id', Integer)
	start_time = Column('start_time', DateTime)
	end_time = Column('end_time', DateTime)

class IpGeoLocation(Base):

	# FIXME: Since there is a table dedicated to storing locations, it would
	# make sense to rename this table to IpLocation or something similar, to
	# indicate that this table stores a list of distinct IPs, but not their
	# geographical locations.
	__tablename__ = 'IpGeoLocation'

	# Store ip_addr and country code, with lat/long.
	# We can use 'geopy.geocoders' to lookup state/postal_code data
	# from lat/long.  It may make sense to gather this information at
	# read time.
	# Store by user_id for ease of lookup.
	ip_id = Column('ip_id', Integer, Sequence('ip_id_seq'), index=True, primary_key=True)
	user_id = Column('user_id', Integer, ForeignKey("Users.user_id"), index=True, nullable=False)
	ip_addr = Column('ip_addr', String(64), index=True)
	country_code = Column('country_code', String(8))
	latitude = Column('latitude', Float())
	longitude = Column('longitude', Float())
	location_id = Column('location_id', Integer, nullable=True, index=True)

class Location(Base):

	__tablename__ = 'Location'

	# Stores a list of distinct locations of users,
	# by lat/long coordinates.
	# Each location has a unique ID.
	location_id = Column('location_id', Integer, Sequence('location_id_seq'), primary_key=True)
	latitude = Column('latitude', String(64))
	longitude = Column('longitude', String(64))
	city = Column('city', String(64))
	state = Column('state', String(64))
	country = Column('country', String(64))

class UserAgents(Base):

	__tablename__ = 'UserAgents'

	user_agent_id = Column('user_agent_id', Integer, Sequence('user_agent_id_seq'), index=True, primary_key=True)
	# Indexing this large column could be fairly expensive.  Does it get us anything,
	# or should we rely on a full column scan before inserting (perhaps also expensive)?
	# Another alternative would be to hash this value in another column and just check that.
	# If we do so, would we have to worry about collisions between unequal user-agents?
	user_agent = Column('user_agent', String(512), unique=True, index=True, nullable=False)
