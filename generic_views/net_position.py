from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import StockNetPositionConfig
from ..models import NavLink

class NetPositionView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = NavLink.objects.get(path=self.request.path).title
        context['nav_links'] = NavLink.objects.order_by('pub_date').all()
        context['buttons'] = []

        context['columns'] = [
            {'attribute_name': 'stock_name', 'column_name': 'Stock Name'},
            {'attribute_name': 'average_quote', 'column_name': 'Average Quote'},
            {'attribute_name': 'revaluation_quote', 'column_name': 'Revaluation Quote'},
            {'attribute_name': 'amount', 'column_name': 'Amount'},
            {'attribute_name': 'profit_loss', 'column_name': 'Profit/Loss'},
        ]

        return context
