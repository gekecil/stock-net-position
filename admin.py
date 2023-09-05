from django.contrib import admin
from .models import NavLink
from .models import UserToken

admin.site.register(NavLink)
admin.site.register(UserToken)
