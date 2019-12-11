from django.contrib import admin

# Register your models here.

import xadmin
from . import models

xadmin.site.register(models.Order)
xadmin.site.register(models.OrderDetail)