#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface


class IDatabaseCreator(interface.Interface):
    """
    Marker interface for database creators
    """


class IAnalyticsDatabase(interface.Interface):
    """
    An utility interface for the Analytics database
    """
    
    engine = interface.Attribute("SQLAlchemy engine")
    session = interface.Attribute("SQLAlchemy session")
    sessionmaker = interface.Attribute("SQLAlchemy session maker")


class IAnalyticsDB(IAnalyticsDatabase):
    """
    BWC Interface for the Analytics DB
    """


class IAnalyticsDSIdentifier(interface.Interface):
    """
    A utility that gets dataserver identities for objects
    and dataserver objects from identities.
    """

    def get_id(obj):
        """
        For the given dataserver object, return a unique
        dataserver identifier.
        """

    def get_object(obj_id):
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

    def __call__(rc_id):  # pylint: disable=no-self-argument,signature-differs
        """
        return the root context for the specified id
        """


class IAnalyticsNTIIDFinder(interface.Interface):
    """
    A utility that finds a dataserver object based on an NTIID
    """

    def find(ntiid):
        """
        For the given dataserver object for the specified ntiid
        """
