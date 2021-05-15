import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from bitcoin_arbitrage.models import Spread, Tri_Spread
from bitcoin_arbitrage.api.mixins import MonitorMixin

from .serializers import (
    ActionSerialier,
    serialize_change
)


logger = logging.getLogger(__name__)


# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~
# Spread endpoints.
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~


class RealTimeSpreadEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            all_spreads = []
            for spread in Spread.objects.all().order_by('-recorded_date')[:5]:
                xchange_buy = spread.xchange_buy
                xchange_sell = spread.xchange_sell
                all_spreads.append({
                    "id": spread.pk,
                    "exchange_buy_id": spread.exchange_buy_id,
                    "exchange_sell_id": spread.exchange_sell_id,
                    "xchange_buy": serialize_change(xchange_buy),
                    "xchange_sell": serialize_change(xchange_sell),
                    "recorded_date": spread.recorded_date,
                    "spread": spread.spread
                })
        except Exception as error:
            logger.exception(str(error))
            return Response({"status": "error"}, status=400)
        return Response({"spreads": all_spreads}, status=200)


class TriSpread(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            tri_spreads = []
            for spread in Tri_Spread.objects.all().order_by('-recorded_date'):
                tri_xchange_buy1 = spread.tri_xchange_buy1
                tri_xchange_buy2 = spread.tri_xchange_buy2
                tri_xchange_sell = spread.tri_xchange_sell
                tri_spreads.append({
                    "id": spread.pk,
                    "tri_exchange_buy1_id": spread.tri_exchange_buy1_id,
                    "tri_exchange_sell_id": spread.tri_exchange_sell_id,
                    "tri_exchange_buy2_id": spread.tri_exchange_buy2_id,
                    "tri_xchange_buy1": serialize_change(tri_xchange_buy1),
                    "tri_xchange_buy2": serialize_change(tri_xchange_buy2),
                    "tri_xchange_sell": serialize_change(tri_xchange_sell),
                    "recorded_date": spread.recorded_date,
                    "tri_spread": spread.tri_spread
                })
        except Exception as error:
            logger.exception(str(error))
            return Response({"status": "error"}, status=400)
        return Response({"tri_spreads": tri_spreads}, status=200)


# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~
# Monitor Endpoints 
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~


class TriangularMonitor(APIView, MonitorMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_name = "trinangular_monitor.txt"
        username = request.user.username
        kwargs = {
            "file": file_name,
            "monitor": "start_tri",
            "user": username
        }

        serializer = ActionSerialier(data=request.data)
        if serializer.is_valid():
            action = serializer.data.get("action")

            if action == "start":
                if self.start_monitor(**kwargs):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "error"}, status=400)

            elif action == "stop":
                if self.stop_monitor(username, file_name):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "success"}, status=200)

            return Response({"status": "error"}, status=400)
        return Response({"status": serializer.errors}, status=400)


class InterExchangeMonitor(APIView, MonitorMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_name = "inter_exchange_monitor.txt"
        username = request.user.username
        kwargs = {
            "file": file_name,
            "monitor": "start_tri",
            "user": username
        }

        serializer = ActionSerialier(data=request.data)
        if serializer.is_valid():
            action = serializer.data.get("action")

            if action == "start":
                if self.start_monitor(**kwargs):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "error"}, status=400)

            elif action == "stop":
                if self.stop_monitor(username, file_name):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "error"}, status=400)

            return Response({"status": "error"}, status=400)
        return Response({"status": serializer.errors}, status=400)


class StrategyBacktestMonitor(APIView, MonitorMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_name = "strategy_back_test_monitor.txt"
        username = request.user.username
        kwargs = {
            "file": file_name,
            "monitor": "start_backtest",
            "user": username
        }

        serializer = ActionSerialier(data=request.data)
        if serializer.is_valid():
            action = serializer.data.get("action")

            if action == "start":
                if self.start_monitor(**kwargs):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "success"}, status=200)

            elif action == "stop":
                if self.stop_monitor(username, file_name):
                    return Response({"status": "success"}, status=200)
                return Response({"status": "error"}, status=400)

            return Response({"status": "error"}, status=400)
        return Response({"status": serializer.errors}, status=400)
