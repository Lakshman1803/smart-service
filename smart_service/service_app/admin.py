from django.contrib import admin
from .models import Employee, Worker, Customer, Vehicle, ServiceRequest, WorkAssignment, Payment, Notification, OTP


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'mobile', 'role', 'is_active']
    search_fields = ['employee_id', 'name', 'mobile']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'is_available']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'email', 'created_at']
    search_fields = ['name', 'mobile']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'brand', 'model', 'vehicle_type', 'customer']
    search_fields = ['vehicle_number', 'brand']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'customer', 'vehicle', 'service_type', 'status', 'estimated_amount', 'created_at']
    list_filter = ['status', 'service_type']
    search_fields = ['tracking_id', 'customer__name', 'vehicle__vehicle_number']


@admin.register(WorkAssignment)
class WorkAssignmentAdmin(admin.ModelAdmin):
    list_display = ['service_request', 'worker', 'assigned_by', 'is_completed', 'assigned_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'service_request', 'amount', 'method', 'status', 'paid_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'message', 'is_read', 'created_at']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'otp', 'purpose', 'is_used', 'created_at']
