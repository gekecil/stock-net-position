from django.db import models
from django.conf import settings
from django.utils import timezone

class PrefixUrl(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=256)
    icon_class = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.url

class Stock(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='stock name')
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.name

class Exchange(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='amount')
    buy_sell = models.CharField(max_length=32, choices=[('buy', 'Buy'), ('sell', 'Sell')], verbose_name='buy/sell')
    pub_date = models.DateTimeField('date published', default=timezone.now)
