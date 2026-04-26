from django.contrib import admin
from .models import ServiceCenter, Holiday, ServiceType, ContactMessage


@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'district', 'state', 'phone', 'is_active']
    list_filter = ['state', 'district', 'is_active']
    search_fields = ['name', 'city', 'district', 'phone']
    list_editable = ['is_active']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'is_national']
    list_filter = ['is_national']
    date_hierarchy = 'date'


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'base_price', 'estimated_duration', 'is_active']
    list_filter = ['vehicle_type', 'is_active']
    list_editable = ['is_active', 'base_price']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'subject', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
