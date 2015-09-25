#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine as sqlalchemy_create_engine

from nti.analytics_database import Base

# import in order to create tables
from nti.analytics_database.assessments import AssignmentViews

from nti.analytics_database.blogs import BlogsCreated

from nti.analytics_database.boards import TopicsViewed

from nti.analytics_database.enrollments import CourseCatalogViews

from nti.analytics_database.profile_views import EntityProfileViews

from nti.analytics_database.resource_tags import NotesCreated

from nti.analytics_database.resource_views import VideoEvents

from nti.analytics_database.resources import Resources

from nti.analytics_database.root_context import RootContextId

from nti.analytics_database.sessions import Sessions

from nti.analytics_database.social import ChatsJoined

from nti.analytics_database.surveys import SurveysTaken

from nti.analytics_database.users import Users

def create_engine(dburi='sqlite://', pool_size=30, max_overflow=10, pool_recycle=300):    
    try:
        if dburi == 'sqlite://':
            result = sqlalchemy_create_engine(dburi,
                                              connect_args={'check_same_thread':False},
                                              poolclass=StaticPool)

        else:
            result = sqlalchemy_create_engine( dburi,
                                               pool_size=pool_size,
                                               max_overflow=max_overflow,
                                               pool_recycle=pool_recycle)
    except TypeError:
        # SQLite does not use pooling anymore.
        result = sqlalchemy_create_engine(dburi)
    return result

def create_sessionmaker(engine, autoflush=False, twophase=False):
    result = sessionmaker(bind=engine,
                          autoflush=autoflush,
                          twophase=twophase)
    return result

def create_session(sessionmaker):
    return scoped_session(sessionmaker)

class AnalyticsDatabaseTest(unittest.TestCase):
    
    def setUp(self):
        self.engine = create_engine()
        self.metadata = getattr(Base, 'metadata')
        self.metadata.create_all(bind=self.engine)
        self.sessionmaker = create_sessionmaker(self.engine)
        self.session = create_session(self.sessionmaker)

    def tearDown(self):
        self.session.close()
