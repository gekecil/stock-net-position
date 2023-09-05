from django.db.models import Model, CharField, IntegerField, DateTimeField, ForeignKey, CASCADE
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .apps import StockNetPositionConfig

class NavLink(Model):
    title = CharField(max_length=128)
    path = CharField(max_length=256)
    icon_class = CharField(max_length=128)
    date_created = DateTimeField('date published')

    def __str__(self):
        return self.path

class UserToken(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    access_token = CharField(max_length=128)
    token_type = CharField(max_length=32)
    url = CharField(max_length=128)
    date_created = DateTimeField('date created')

    def __str__(self):
        return '%s %s' % (self.token_type, self.access_token)

class Stock(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    name = CharField(max_length=128)
    pub_date = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return None

class Exchange(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    stock = ForeignKey(Stock, on_delete=CASCADE, verbose_name='stock name')
    quote = IntegerField('quote')
    amount = IntegerField('amount')
    purchase_sale = CharField(max_length=32, verbose_name='Purchase/Sale')
    pub_date = DateTimeField('Purchase/Sale date', default=timezone.now)

    def get_absolute_url(self):
        view_name = '%s:update-stock-exchange' % StockNetPositionConfig.name

        return reverse(view_name, kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.stock.pk is None and not Stock.objects.filter(name=self.stock.name).exists():
            Stock(name=self.stock.name, auth_user=self.auth_user).save()

        if not self._state.adding:
            original = self.__class__.objects.get(pk=self.pk)

            if self.stock.name != original.stock.name and self.__class__.objects.filter(stock__name=original.stock.name).count() == 1:
                original.stock.delete()

        if self.stock.pk is None:
            self.stock = Stock.objects.get(name=self.stock.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        if not self.__class__.objects.filter(stock=self.stock).exists():
            self.stock.delete()
