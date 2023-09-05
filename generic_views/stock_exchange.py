from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import modelform_factory, inlineformset_factory, TextInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import resolve, reverse_lazy
from ..apps import StockNetPositionConfig
from ..models import NavLink, Stock, Exchange

class StockExchangeListView(LoginRequiredMixin, ListView):
    model = Exchange
    ordering = ['-pub_date']
    template_name = 'contents/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, StockNetPositionConfig.verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {'name': 'Purchase', 'path': self.request.path+'/purchase'},
            {'name': 'Sale', 'path': self.request.path+'/sale'},
        ]

        context['fields'] = ['stock', 'quote', 'amount', 'purchase_sale', 'auth_user', 'pub_date']

        return context

class StockExchangeUpdateView(LoginRequiredMixin, UpdateView):
    model = Exchange
    fields = ['stock', 'quote', 'amount']
    template_name = 'contents/single-form.html'
    success_url = reverse_lazy('%s:%s' % (StockNetPositionConfig.name, 'stock-exchange'))

    def get_form(self):
        form = super(StockExchangeUpdateView, self).get_form()

        form.fields['quote'].widget.attrs.update({'class': 'form-control'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control'})

        if 'stock' in form.fields:
            form.fields['stock'].widget.attrs.update({'class': 'form-select'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = modelform_factory(
            Stock,
            fields=('name', ),
            widgets={
                'name': TextInput(attrs={'class': 'form-control'}),
            }
        )

        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Update Stock Exchange - %s' % (StockNetPositionConfig.verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['forms'] = [form(instance=self.get_object().stock), self.get_form()]
        context['can_delete'] = True

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        if 'stock' not in form.fields:
            form.instance.stock = Stock(name=self.request.POST.get('name'), auth_user=self.request.user)

        return super().form_valid(form)

class StockExchangeDeleteView(LoginRequiredMixin, DeleteView):
    model = Exchange
    template_name = 'contents/confirm-delete.html'
    success_url = reverse_lazy('%s:%s' % (StockNetPositionConfig.name, 'stock-exchange'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Delete Stock Exchange - %s' % (StockNetPositionConfig.verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

class StockExchangePurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Exchange
    fields = ['quote', 'amount']
    template_name = 'contents/relational-form.html'
    success_url = reverse_lazy('%s:%s' % (StockNetPositionConfig.name, 'stock-exchange'))

    def get_form(self):
        form = super(StockExchangePurchaseCreateView, self).get_form()

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = modelform_factory(
            Stock,
            fields=('name', ),
            widgets={
                'name': TextInput(attrs={'class': 'form-control'}),
            }
        )

        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Stock Exchange Purchase - %s' % (StockNetPositionConfig.verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['forms'] = [form(), self.get_form()]

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user
        form.instance.stock = Stock(name=self.request.POST.get('name'), auth_user=self.request.user)
        form.instance.purchase_sale = 'purchase'

        return super().form_valid(form)

class StockExchangeSaleCreateView(LoginRequiredMixin, CreateView):
    model = Exchange
    fields = ['stock', 'quote', 'amount']
    template_name = 'contents/single-form.html'
    success_url = reverse_lazy('%s:%s' % (StockNetPositionConfig.name, 'stock-exchange'))

    def get_form(self):
        form = super(StockExchangeSaleCreateView, self).get_form()

        form.fields['stock'].widget.attrs.update({'class': 'form-select'})
        form.fields['quote'].widget.attrs.update({'class': 'form-control'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Stock Exchange Sale - %s' % (StockNetPositionConfig.verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user
        form.instance.purchase_sale = 'sale'

        return super().form_valid(form)
