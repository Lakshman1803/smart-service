from django.contrib import admin
from .models import RepairIssue, Vehicle, TimeSlot, Booking, RepairCharge, ServiceRecord, WorkAssignment


@admin.register(RepairIssue)
class RepairIssueAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'category', 'estimated_cost_min', 'estimated_cost_max', 'is_active']
    list_filter = ['vehicle_type', 'category', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']
    ordering = ['vehicle_type', 'category', 'display_order']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'owner', 'vehicle_type', 'make', 'model', 'year']
    search_fields = ['vehicle_number', 'owner__mobile_number', 'make', 'model']
    list_filter = ['vehicle_type', 'fuel_type']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['service_center', 'date', 'start_time', 'end_time', 'max_bookings', 'current_bookings', 'is_available']
    list_filter = ['service_center', 'date', 'is_available']
    list_editable = ['is_available', 'max_bookings']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'customer', 'vehicle', 'service_center', 'booking_date', 'status', 'booking_type', 'estimated_total']
    list_filter = ['status', 'booking_type', 'service_center']
    search_fields = ['booking_id', 'customer__mobile_number', 'vehicle__vehicle_number']
    date_hierarchy = 'booking_date'
    filter_horizontal = ['selected_issues', 'service_types', 'assigned_workers']


@admin.register(RepairCharge)
class RepairChargeAdmin(admin.ModelAdmin):
    list_display = ['booking', 'description', 'charge_type', 'quantity', 'unit_price', 'total', 'is_extra', 'added_by']
    list_filter = ['charge_type', 'is_extra']
    search_fields = ['description', 'booking__booking_id']


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ['booking', 'vehicle', 'employee', 'completed_at']


@admin.register(WorkAssignment)
class WorkAssignmentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'worker', 'status', 'assigned_at']
    list_filter = ['status']
