from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('net-position', views.net_position, name='net-position'),
    path('stock-exchange', views.stock_exchange, name='stock-exchange'),
    path('stock-exchange/<int:pk>', views.detail_stock_exchange, name='detail-stock-exchange'),
    path('stock-exchange/<int:pk>/update', views.update_stock_exchange, name='update-stock-exchange'),
    path('stock-exchange/<int:pk>/delete', views.delete_stock_exchange, name='delete-stock-exchange'),
    path('stock-exchange/purchase', views.stock_exchange_purchase, name='stock-exchange-purchase'),
    path('stock-exchange/sale', views.stock_exchange_sale, name='stock-exchange-sale'),
]
