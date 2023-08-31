from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import StockNetPositionConfig
from ..models import NavLink, Exchange

class StockExchangeListView(LoginRequiredMixin, ListView):
    model = Exchange
    template_name = 'contents/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = NavLink.objects.get(path=self.request.path).title
        context['nav_links'] = NavLink.objects.order_by('pub_date').all()

        context['buttons'] = [
            {'name': 'Create Position', 'path': self.request.path+'/create'},
        ]

        context['columns'] = [
            {'attribute_name': 'name', 'column_name': 'Position'},
            {'attribute_name': 'pub_date', 'column_name': 'Publication Date'},
        ]

        return context

class StockExchangeUpdateView(LoginRequiredMixin, UpdateView):
    model = Exchange
    template_name = 'contents/single-form.html'
    fields = ['stock']

class StockExchangePurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Exchange
    template_name = 'contents/single-form.html'
    fields = ['stock']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Create Position'
        context['nav_links'] = NavLink.objects.order_by('pub_date').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(StockNetPositionConfig.name+':positions')

class StockExchangeSaleCreateView(LoginRequiredMixin, CreateView):
    model = Exchange
    template_name = 'contents/single-form.html'
    fields = ['stock']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Create Position'
        context['nav_links'] = NavLink.objects.order_by('pub_date').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(StockNetPositionConfig.name+':positions')
