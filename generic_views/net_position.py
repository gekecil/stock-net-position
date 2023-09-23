import requests
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.db.models import F, Value, Sum
from django.db.models.functions import Coalesce
from ..models import NavLink, UserToken, Stock, Exchange

class NetPositionListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'contents/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        authorization = UserToken.objects.get(auth_user=self.request.user)
        quotes_request = requests.get(authorization.url, headers={'Authorization': str(authorization)})

        for obj in queryset:
            exchange = Exchange.objects.order_by('date_updated').filter(stock=obj)
            exchange_purchase = exchange.filter(purchase_sale='purchase').annotate(amount_quote=F('amount') * F('quote')).aggregate(amount_quote_sum=Coalesce(Sum('amount_quote'), Value(0)), volume=Coalesce(Sum('amount'), Value(0)))
            exchange_sale = exchange.filter(purchase_sale='sale').annotate(amount_quote=-F('amount') * F('quote')).aggregate(amount_quote_sum=Coalesce(Sum('amount_quote'), Value(0)), volume=-Coalesce(Sum('amount'), Value(0)))

            obj.current_volume = exchange_purchase['volume'] + exchange_sale['volume']
            obj.average_quote = None
            obj.revaluation_quote = None
            obj.profit_loss = None

            if exchange_purchase['volume'] != 0:
                obj.average_quote = exchange_purchase['amount_quote_sum'] / exchange_purchase['volume']

            if exchange_sale['volume'] != 0 and obj.average_quote is not None:
                obj.average_quote = obj.average_quote + (
                    exchange_sale['amount_quote_sum'] / exchange_sale['volume']
                )

                obj.average_quote = obj.average_quote / 2

            if quotes_request.status_code == 200:
                obj.revaluation_quote = quotes_request.json()
                obj.revaluation_quote = filter(lambda quote: quote['name'] == obj.name, obj.revaluation_quote['data'])
                obj.revaluation_quote = list(obj.revaluation_quote)
                obj.revaluation_quote = obj.revaluation_quote[0]['quote']

            if obj.revaluation_quote is not None and obj.average_quote is not None:
                obj.profit_loss = (obj.revaluation_quote - obj.average_quote) * obj.current_volume

        queryset.average_quote__verbose_name = 'average quote'
        queryset.revaluation_quote__verbose_name = 'revaluation quote'
        queryset.current_volume__verbose_name = 'current volume'
        queryset.profit_loss__verbose_name = 'profit/loss'

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = []
        context['fields'] = ['name', 'average_quote', 'revaluation_quote', 'current_volume', 'profit_loss']

        return context
