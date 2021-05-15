"""
~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
Monitor testing.
~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
"""

import logging
import os
import pdb

from django.conf import settings
from django.test import TestCase

from rest_framework.test import (
    APIRequestFactory,
    force_authenticate
)

from bitcoin_arbitrage.models import Spread, Tri_Spread, Exchange
from accounts.models import User


from bitcoin_arbitrage.api import views



class TestApi(TestCase):
    
    def setUp(self):
        self.bad_data = {}
        self.good_data = {}
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="Tes4Pa$sword",
            username="test_user"
        )
        self.action_start = {"action": "start"}
        self.action_stop = {"action": "stop"}


    def test_triangular_monitor(self):
        start_triangular_monitor = views.TriangularMonitor.as_view()
        url = "api/v1/arbitrage/triangular-monitor"        
        request = self.factory.post(url, data={"action" : "start"})
        force_authenticate(request, user=self.user)
        response = start_triangular_monitor(request)
        self.assertTrue(response.status_code == 200)  
        get_tri_spread = views.TriSpread.as_view()
        url = "api/v1/arbitrage/triangular-exchange-realtime"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = get_tri_spread(request)
        self.assertTrue(response.status_code == 200)
        stop_triangular_monitor = views.TriangularMonitor.as_view()
        url = "api/v1/arbitrage/triangular-monitor"
        request = self.factory.post(url, data={"action" : "stop"})
        force_authenticate(request, user=self.user)
        response = stop_triangular_monitor(request)
        self.assertTrue(response.status_code == 200) 
        pdb.set_trace()

    def test_two_monitors_same_user(self):
        pass


        

 




