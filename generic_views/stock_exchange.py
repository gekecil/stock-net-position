from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.forms import TextInput
from django.urls import reverse
from ..models import NavLink, Stock, Exchange

class StockExchangeListView(LoginRequiredMixin, ListView):
    model = Exchange
    ordering = ['-date_updated']
    template_name = 'contents/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        for obj in queryset:
            obj.view_name = '%s:detail-stock-exchange' % self.request.resolver_match.app_name

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {'name': 'Purchase', 'path': self.request.path+'/purchase'},
            {'name': 'Sale', 'path': self.request.path+'/sale'},
        ]

        context['fields'] = ['stock', 'quote', 'amount', 'purchase_sale', 'date_created', 'date_updated']

        return context

class StockExchangeDetailView(LoginRequiredMixin, DetailView):
    model = Exchange
    template_name = 'contents/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Detail Stock Exchange - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {
                'name': 'update stock exchange',
                'url': reverse('%s:update-stock-exchange' % self.request.resolver_match.app_name, kwargs={'pk': self.get_object().pk}),
                'color': 'primary',
            },
            {
                'name': 'delete',
                'url': reverse('%s:delete-stock-exchange' % self.request.resolver_match.app_name, kwargs={'pk': self.get_object().pk}),
                'color': 'danger',
            },
        ]

        context['fields'] = ['stock', 'quote', 'amount', 'purchase_sale', 'auth_user', 'date_created', 'date_updated']

        return context

class StockExchangeUpdateView(LoginRequiredMixin, UpdateView):
    model = Exchange
    fields = ['stock', 'quote', 'amount']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super(__class__, self).get_form()

        form.fields['quote'].widget.attrs.update({'class': 'form-control'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control'})

        if form.instance.purchase_sale == 'purchase':
            form.fields['stock'].widget = TextInput(attrs={'class': 'form-control', 'readonly': True})

        else:
            form.fields['stock'].widget.attrs.update({'class': 'form-select'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Update Stock Exchange - %s' % (apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        if form.instance.purchase_sale == 'purchase':
            form.instance.stock = Stock(name=self.request.POST.get('stock'), auth_user=self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:stock-exchange' % self.request.resolver_match.app_name)

class StockExchangeDeleteView(LoginRequiredMixin, DeleteView):
    model = Exchange
    template_name = 'contents/confirm-delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Delete Stock Exchange - %s' % (apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def get_success_url(self):
        return reverse('%s:stock-exchange' % self.request.resolver_match.app_name)

class StockExchangePurchaseView(LoginRequiredMixin, CreateView):
    model = Exchange
    fields = ['stock', 'quote', 'amount']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super(__class__, self).get_form()

        form.fields['stock'].widget = TextInput()

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Stock Exchange Purchase - %s' % (apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user
        form.instance.stock = Stock(name=self.request.POST.get('stock'), auth_user=self.request.user)
        form.instance.purchase_sale = 'purchase'

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:stock-exchange' % self.request.resolver_match.app_name)

class StockExchangeSaleView(LoginRequiredMixin, CreateView):
    model = Exchange
    fields = ['stock', 'quote', 'amount']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super(__class__, self).get_form()

        form.fields['stock'].widget.attrs.update({'class': 'form-select'})
        form.fields['quote'].widget.attrs.update({'class': 'form-control'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Stock Exchange Sale - %s' % (apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user
        form.instance.purchase_sale = 'sale'

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:stock-exchange' % self.request.resolver_match.app_name)
