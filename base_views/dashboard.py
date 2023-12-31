from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.db.models import F, Value, Sum
from django.db.models.functions import Coalesce
from ..models import NavLink, Exchange

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exchange = Exchange.objects.filter(purchase_sale='sale')
        chart_labels = exchange.order_by('date_updated')
        chart_labels = chart_labels[:50]
        line_chart = {'datasets': []}

        if chart_labels.exists():
            stocks = exchange.filter(purchase_sale='sale', date_updated__gte=chart_labels[0].date_updated).distinct('stock')

            for stock in stocks:
                line_chart['datasets'].append({'label': stock.stock.name})

            for key, dataset in enumerate(line_chart['datasets']):
                for chart_label in chart_labels.values_list('date_updated__date', flat=True):
                    dataset_data = 0
                    sale_amount = exchange.filter(stock=stocks[key].stock, purchase_sale='sale', date_updated__date=chart_label).aggregate(Sum('amount')).get('amount__sum')
                    exchange_purchase = Exchange.objects.order_by('-date_updated').filter(stock=stocks[key].stock, purchase_sale='purchase', date_updated__date__lte=chart_label)
                    exchange_purchase_key = 0

                    while exchange_purchase_key < exchange_purchase.count() and exchange_purchase[exchange_purchase_key].amount < sale_amount:
                        exchange_purchase_key = exchange_purchase_key + 1

                    exchange_purchase = exchange_purchase[:exchange_purchase_key+1].annotate(amount_quote=F('amount') * F('quote')).aggregate(amount_quote_sum=Coalesce(Sum('amount_quote'), Value(0)), volume=Coalesce(Sum('amount'), Value(0)))

                    if exchange_purchase['volume'] != 0:
                        dataset_data = exchange.filter(stock=stocks[key].stock)[:50].annotate(profit_loss=(F('quote') - Value(exchange_purchase['amount_quote_sum'] / exchange_purchase['volume'])) * F('amount')).aggregate(Sum('profit_loss')).get('profit_loss__sum')

                    if 'data' not in dataset:
                        dataset['data'] = {
                            chart_label.strftime('%d %b %Y'): dataset_data
                        }

                    else:
                        dataset['data'][chart_label.strftime('%d %b %Y')] = dataset_data

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['line_chart'] = line_chart

        return context
