from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'created', 'updated')
    search_fields = ('name', 'vendor_code')
    list_filter = ('created', 'updated')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status', 'created', 'updated')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status', 'order_date', 'delivery_date', 'created', 'updated')
    raw_id_fields = ('vendor',)

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('vendor__name',)
    list_filter = ('date',)

