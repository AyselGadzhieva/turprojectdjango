from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'need_for_a_visa', 'need_a_passport', 'visa_cost', 'pas_cost')
    list_editable = ('need_for_a_visa', 'need_a_passport')

    search_fields = ('name',)
    list_filter = ('need_for_a_visa', 'need_a_passport',)


@admin.register(models.Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_id')


@admin.register(models.Meansoftransport)
class MeansoftransportAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WaypointsAdmin(admin.TabularInline):
    model = models.Waypoints
    extra = 0


@admin.register(models.Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_editable = ('active',)

    list_filter = ('active',)

    inlines = [WaypointsAdmin]


@admin.register(models.Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'begin_date', 'end_date', 'route_id', 'active')
    list_editable = ('active',)

    search_fields = ('name', 'price')


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone', 'registedate')
    search_fields = ('surname', 'name', 'patronymic')


@admin.register(models.Sellpermit)
class SellpermitAdmin(admin.ModelAdmin):
    list_display = ('permit_id', 'date_time_sale', 'price', 'price_disc', 'client_id')
