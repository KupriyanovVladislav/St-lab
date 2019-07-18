from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Shop, Department, Item, Statistics


class ShopAdmin(ModelAdmin):
    list_display = ('name', 'address', 'staff_amount')


class DepartmentAdmin(ModelAdmin):
    list_display = ('sphere', 'staff_amount', 'shop')


class ItemAdmin(ModelAdmin):
    list_display = ('name', 'description', 'price', 'is_sold', 'comments', 'department')


class StatisticsAdmin(ModelAdmin):
    list_display = ('url', 'amount')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Statistics, StatisticsAdmin)
