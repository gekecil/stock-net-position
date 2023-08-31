from django.urls import path
from . import apps, views

app_name = apps.StockNetPositionConfig.name

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('net-position', views.net_position, name='net-position'),
    path('stock-exchange', views.stock_exchange, name='stock-exchange'),
    path('stock-exchange/<int:id>/update', views.update_stock_exchange, name='update-stock-exchange'),
    path('stock-exchange/purchase', views.stock_exchange_purchase, name='stock-exchange-purchase'),
    path('stock-exchange/sale', views.stock_exchange_sale, name='stock-exchange-sale'),
]
