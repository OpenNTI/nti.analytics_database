#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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

# Init so these exist in our Base
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
