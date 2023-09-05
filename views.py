from .base_views.dashboard import DashboardView
from .generic_views.net_position import NetPositionListView
from .generic_views.stock_exchange import StockExchangeListView, StockExchangeUpdateView, StockExchangeDeleteView, StockExchangePurchaseCreateView, StockExchangeSaleCreateView
from .models import Exchange

def dashboard(request):
    return DashboardView.as_view()(request)

def net_position(request):
    return NetPositionListView.as_view()(request)

def stock_exchange(request):
    return StockExchangeListView.as_view()(request)

def update_stock_exchange(request, pk):
    if Exchange.objects.get(id=pk).purchase_sale == 'purchase':
        return StockExchangeUpdateView.as_view(fields=['quote', 'amount'], template_name='contents/relational-form.html')(request, pk=pk)

    return StockExchangeUpdateView.as_view()(request, pk=pk)

def delete_stock_exchange(request, pk):
    return StockExchangeDeleteView.as_view()(request, pk=pk)

def stock_exchange_purchase(request):
    return StockExchangePurchaseCreateView.as_view()(request)

def stock_exchange_sale(request):
    return StockExchangeSaleCreateView.as_view()(request)
