#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# The column type for session ids
SESSION_COLUMN_TYPE = Integer

#: The column type for NTIIDs; max length of 160 as of 8.1.14
NTIID_COLUMN_TYPE = String(256)

#: The column type for IntIds
INTID_COLUMN_TYPE = BigInteger

#: The character used to separate context path elements on storage.
#: '/' is illegal in ntiid strings
CONTEXT_PATH_SEPARATOR = '/'
