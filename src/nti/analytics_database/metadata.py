#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database import Base


class AnalyticsMetadata(object):

    def __init__(self, engine):
        logger.info("Initializing database")
        getattr(Base, 'metadata').create_all(engine)
