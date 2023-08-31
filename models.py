from django.db import models
from django.conf import settings
from django.utils import timezone

class NavLink(models.Model):
    title = models.CharField(max_length=128)
    path = models.CharField(max_length=256)
    icon_class = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.path

class Stock(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='stock name')
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.name

class Exchange(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    purchase_quote = models.IntegerField(verbose_name='purchase quote')
    sale_quote = models.IntegerField(null=True, verbose_name='sale quote')
    amount = models.IntegerField(verbose_name='amount')
    purchase_sale = models.CharField(max_length=32, choices=[('purchase', 'Purchase'), ('sale', 'Sale')], verbose_name='Purchase/Sale')
    pub_date = models.DateTimeField('date published', default=timezone.now)
