#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy.schema import Sequence

from nti.analytics_database import Base

from nti.analytics_database.meta_mixins import BaseTableMixin
from nti.analytics_database.meta_mixins import RootContextMixin

logger = __import__('logging').getLogger(__name__)


class SearchQueries(Base, BaseTableMixin, RootContextMixin):

    __tablename__ = 'SearchQueries'

    query_elapsed_time = Column('query_elapsed_time', Float,
                                nullable=True, index=False)

    search_query_id = Column('search_query_id', Integer,
                             Sequence('search_query_seq'),
                             index=True, nullable=False,
                             primary_key=True)

    hit_count = Column('hit_count', Integer, nullable=True, index=True)

    search_types = Column('search_types',
                          String(1024),
                          nullable=True)

    term = Column('term', String(256),
                  nullable=True, index=True)

    @property
    def SearchTypes(self):
        return self.search_types.split('/') if self.search_types else self.search_types
