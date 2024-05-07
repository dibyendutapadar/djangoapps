from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)
    created =   models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='vendors')

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PD','Pending' #name=value,label
        COMPLETED = 'CM', 'Completed'
        CANCELLED = 'CN', 'Canceled'
        

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor,
                               on_delete=models.CASCADE,
                               related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PENDING)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    created =   models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='purchase_orders')


    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"