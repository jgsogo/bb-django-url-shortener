#!/usr/bin/env python
# encoding: utf-8

from django.utils.unittest import TestCase
from django.test.client import RequestFactory, Client

from shortener.models import Link
from shortener_data.models import RequestData, UserAgent
from shortener_data.views import robots

class RequestsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.link = Link.create('http://thisis.valid.url/to/test/')
        self.c = Client()

    def test_request_creation(self):
        # User agent strings: http://www.user-agents.org/allagents.xml
        uas = ( ('browser','Sunrise XP/2.x'),
                ('other', 'suchpadbot/1.0 (+http://www.suchpad.de)'),
                ('other','TulipChain/5.x (http://ostermiller.org/tulipchain/) Java/1.x.1_0x (http://java.sun.com/) Linux/2.4.17'),
                ('other', 'TulipChain/5.xx (http://ostermiller.org/tulipchain/) Java/1.x.1_0x (http://apple.com/) Mac_OS_X/10.2.8'),
                ('browser', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5)'),
                )
        for ua in uas:
            request = self.factory.get('/%s' % self.link._hash, HTTP_USER_AGENT=ua[1])
            request_data = RequestData.create(request, self.link)
            # TODO: write actual test.

    def test_robots(self):
        uas = 'Advanced Browser (http://www.avantbrowser.com)'
        request = self.factory.get('/%s' % self.link._hash, HTTP_USER_AGENT=uas)

        # Two 'human' visits ==> human
        request_data = RequestData.create(request, self.link)
        request_data = RequestData.create(request, self.link)
        self.assertEqual(request_data.user_agent._hit_robots, 0)
        self.assertTrue(request_data.user_agent.is_human)

        # One 'robots' visit ==> human
        robots(request)
        user_agent = UserAgent.objects.get(user_agent_string=uas)
        self.assertEqual(user_agent._hit_robots, 1)
        self.assertTrue(user_agent.is_human)

        # Another one 'robots' visit ==> robot
        robots(request)
        user_agent = UserAgent.objects.get(user_agent_string=uas)
        self.assertEqual(user_agent._hit_robots, 2)
        self.assertFalse(user_agent.is_human)

