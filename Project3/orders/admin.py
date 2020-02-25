from django.contrib import admin

from .models import Salad, Pasta, DinnerPlatter, Sub1, Sub2, Pizza, MenuItem,\
OrderItem, Order

# Register your models here.
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(DinnerPlatter)
admin.site.register(Sub1)
admin.site.register(Sub2)
admin.site.register(Pizza)
admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Order)
