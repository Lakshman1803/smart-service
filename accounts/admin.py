from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Employee, OTPVerification, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['mobile_number', 'first_name', 'last_name', 'role', 'is_verified', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['mobile_number', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_photo', 'address', 'city', 'pincode')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('mobile_number', 'password1', 'password2', 'role')}),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'designation', 'service_center', 'is_active']
    list_filter = ['designation', 'is_active', 'service_center']
    search_fields = ['employee_id', 'user__first_name', 'user__mobile_number']


@admin.register(OTPVerification)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'otp', 'purpose', 'is_used', 'created_at']
    list_filter = ['purpose', 'is_used']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
