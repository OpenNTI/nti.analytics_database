#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods
# pylint: disable=no-member

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from datetime import datetime

from nti.analytics_database.sessions import Location
from nti.analytics_database.sessions import Sessions
from nti.analytics_database.sessions import IpGeoLocation

from nti.analytics_database.users import Users

from nti.analytics_database.tests import AnalyticsDatabaseTest


class TestSessions(AnalyticsDatabaseTest):

    def test_duration(self):
        session = Sessions()
        now = datetime.now()
        session.end_time = session.start_time = now
        assert_that(session,
                    has_property('Duration', is_(0)))

    def test_coverage(self):
        location = Location(location_id=1,
                            latitude=u'35.2226',
                            longitude=u'97.4395',
                            city=u'Norman',
                            state=u'OK',
                            country=u'USA')
        self.session.add(location)

        user = Users(user_ds_id=1, user_id=1, username=u'ichigo')
        self.session.add(user)

        iploc = IpGeoLocation(ip_id=1, user_id=1, ip_addr=u'10.50.42.228',
                              country_code=u'US',
                              latitude=35.2226, longitude=97.4395, location_id=1)
        self.session.add(iploc)

        session = Sessions(session_id=1, user_id=1, ip_addr=u'10.50.42.228')
        self.session.add(session)
        self.session.commit()

        assert_that(session,
                    has_property('Location', is_(location)))
