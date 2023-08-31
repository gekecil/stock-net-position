from .base_views.dashboard import DashboardView
from .generic_views.net_position import NetPositionView
from .generic_views.stock_exchange import StockExchangeListView, StockExchangeUpdateView, StockExchangePurchaseCreateView, StockExchangeSaleCreateView

def dashboard(request):
    return DashboardView.as_view()(request)

def net_position(request):
    return NetPositionView.as_view()(request)

def stock_exchange(request):
    return StockExchangeListView.as_view()(request)

def update_stock_exchange(request):
    return StockExchangeUpdateView.as_view()(request)

def stock_exchange_purchase(request):
    return StockExchangePurchaseCreateView.as_view()(request)

def stock_exchange_sale(request):
    return StockExchangeSaleCreateView.as_view()(request)
