from django.contrib import admin
from .models import *


class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_number', 'contract')
    list_display_links = ('id', 'order_number')
    search_fields = ('id', 'order_number')


class DetalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_number')
    list_display_links = ('id', 'order_number')
    search_fields = ('id', 'order_number')


admin.site.register(Factory, FactoryAdmin)
admin.site.register(Detal, DetalAdmin)
