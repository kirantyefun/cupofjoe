from django.contrib import admin
from .models import Cafe, MenuItem, Order, OrderItem

admin.site.register(Cafe)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
