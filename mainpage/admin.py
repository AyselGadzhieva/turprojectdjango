from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'need_for_a_visa', 'need_a_passport', 'visa_cost', 'pas_cost')
    search_fields = ('name',)
    list_filter = ('need_for_a_visa', 'need_a_passport',)


@admin.register(models.Locality)
class LocalityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Meansoftransport)
class MeansoftransportAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)


@admin.register(models.Waypoints)
class WaypointsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'begin_date', 'end_date', 'active')
    search_fields = ('name', 'price')


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'registedate')
    search_fields = ('surname', 'name', 'patronymic')


@admin.register(models.Sellpermit)
class SellpermitAdmin(admin.ModelAdmin):
    list_display = ('permit_id', 'date_time_sale', 'price_disc', 'client_id')
