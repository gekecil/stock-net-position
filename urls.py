from django.urls import path
from . import apps
from .views.base_views import DashboardView
from .views.net_position_views import NetPositionListView
from .views.stock_exchange_views import StockExchangeListView

app_name = apps.StockNetPositionConfig.name

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('net-position', NetPositionListView.as_view(), name='net-position'),
    path('stock-exchange', StockExchangeListView.as_view(), name='stock-exchange'),
    #path('stock-exchange/purchase', StockExchangePurchaseView.as_view(), name='stock-exchange-purchase'),
    #path('stock-exchange/sale', StockExchangeSaleView.as_view(), name='stock-exchange-sale'),
]
