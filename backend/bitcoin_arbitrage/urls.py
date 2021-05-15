from django.urls import path
from bitcoin_arbitrage.api import views as api_views

app_name = "bitcoin_arbitrage"

urlpatterns = [
    path(
        route="coinbase-realtime", 
        view=api_views.RealTimeSpreadEndpoint.as_view(), 
        name="realtime_spreads"
    ),
    path(
        route="triangular-exchange-realtime",
        view=api_views.TriSpread.as_view(),
        name="tri_spread"
    ),
    path(
        route="triangular-monitor",
        view=api_views.TriangularMonitor.as_view(),
        name="triangular_monitor"
    ),
    path(
        route="inter-exchange-monitor",
        view=api_views.InterExchangeMonitor.as_view(),
        name="inter_exchange_monitor"
    ),
    path(
        route="strategy-bt-monitor",
        view=api_views.StrategyBacktestMonitor.as_view(),
        name="strategy_bt_monitor"
    )
]
