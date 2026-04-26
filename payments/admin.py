from django.contrib import admin
from .models import Payment, ServiceCharge


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'booking', 'customer', 'issue_charges_total',
                    'extra_charges_total', 'total_amount', 'payment_method', 'payment_status', 'paid_at']
    list_filter = ['payment_method', 'payment_status']
    search_fields = ['receipt_number', 'booking__booking_id', 'customer__mobile_number']
    readonly_fields = ['receipt_number', 'created_at']


@admin.register(ServiceCharge)
class ServiceChargeAdmin(admin.ModelAdmin):
    list_display = ['booking', 'description', 'quantity', 'unit_price', 'total', 'is_extra']
    list_filter = ['is_extra']
