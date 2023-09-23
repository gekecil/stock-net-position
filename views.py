from django.views.generic.base import RedirectView
from .base_views.dashboard import DashboardView
from .generic_views.net_position import NetPositionListView
from .generic_views.stock_exchange import StockExchangeListView, StockExchangeDetailView, StockExchangeUpdateView, StockExchangeDeleteView, StockExchangePurchaseView, StockExchangeSaleView
from .models import Exchange

def home(request):
    app_name = request.resolver_match.app_name
    pattern_name = '%s:dashboard' % app_name

    return RedirectView.as_view(pattern_name=pattern_name)(request)

def dashboard(request):
    return DashboardView.as_view()(request)

def net_position(request):
    return NetPositionListView.as_view()(request)

def stock_exchange(request):
    return StockExchangeListView.as_view()(request)

def detail_stock_exchange(request, pk):
    return StockExchangeDetailView.as_view()(request, pk=pk)

def update_stock_exchange(request, pk):
    return StockExchangeUpdateView.as_view()(request, pk=pk)

def delete_stock_exchange(request, pk):
    return StockExchangeDeleteView.as_view()(request, pk=pk)

def stock_exchange_purchase(request):
    return StockExchangePurchaseView.as_view()(request)

def stock_exchange_sale(request):
    return StockExchangeSaleView.as_view()(request)
