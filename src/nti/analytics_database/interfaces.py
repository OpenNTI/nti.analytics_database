#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

class IAnalyticsDSIdentifier(interface.Interface):
	"""
	A utility that gets dataserver identities for objects
	and dataserver objects from identities.
	"""

	def get_id(self, obj):
		"""
		For the given dataserver object, return a unique
		dataserver identifier.
		"""

	def get_object(self, obj_id):
		"""
		For the given dataserver identifier, return a
		dataserver object.
		"""

class IAnalyticsNTIIDIdentifier(IAnalyticsDSIdentifier):
	"""
	``IAnalyticsDSIdentifier`` for NTIIDs.
	"""

class IAnalyticsIntidIdentifier(IAnalyticsDSIdentifier):
	"""
	``IAnalyticsDSIdentifier`` for ds intids.
	"""

class IAnalyticsRootContextIdentifier(IAnalyticsDSIdentifier):
	"""
	``IAnalyticsDSIdentifier`` for root context objects, which may
	resolve into courses or books.
	"""

class IAnalyticsRootContextResolver(interface.Interface):
	"""
	Marker interface to resolve root context objects
	"""

	def __call__(rc_id):
		pass

