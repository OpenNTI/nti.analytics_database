#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy.schema import Sequence

from zope import component

from nti.analytics_database import INTID_COLUMN_TYPE

from nti.analytics_database import Base

from nti.analytics_database.interfaces import IAnalyticsIntidIdentifier


class Users(Base):

    __tablename__ = 'Users'

    user_id = Column('user_id', Integer, Sequence('user_id_seq'),
                     index=True, nullable=False, primary_key=True)

    user_ds_id = Column('user_ds_id', INTID_COLUMN_TYPE,
                        nullable=True, index=True)

    allow_research = Column('allow_research', Boolean,
                            nullable=True, default=None)

    username = Column('username', String(64), nullable=True,
                      unique=False, index=True)

    username2 = Column('username2', String(64), nullable=True, unique=False)

    create_date = Column('create_date', DateTime, nullable=True)

    @property
    def user(self):
        id_utility = component.getUtility(IAnalyticsIntidIdentifier)
        return id_utility.get_object(self.user_ds_id)
