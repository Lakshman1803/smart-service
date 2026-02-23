from django.db import models
from django.utils import timezone
import random, string


class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=50, default='Service Advisor')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class Worker(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"


class OTP(models.Model):
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=50)  # login, register, verify_vehicle
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        delta = timezone.now() - self.created_at
        return delta.seconds < 300 and not self.is_used  # 5 min expiry

    def __str__(self):
        return f"{self.mobile} - {self.otp}"


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('2W', 'Two Wheeler'),
        ('3W', 'Three Wheeler'),
        ('4W', 'Four Wheeler'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=2, choices=VEHICLE_TYPES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(default=2020)

    def __str__(self):
        return f"{self.vehicle_number} - {self.brand} {self.model}"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OTP_VERIFIED', 'OTP Verified'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DELIVERED', 'Delivered'),
    ]
    SERVICE_TYPES = [
        ('GENERAL', 'General Service'),
        ('OIL_CHANGE', 'Oil Change'),
        ('BRAKE_SERVICE', 'Brake Service'),
        ('TYRE_CHANGE', 'Tyre Change / Rotation'),
        ('AC_SERVICE', 'AC Service'),
        ('BATTERY', 'Battery Check / Replacement'),
        ('WASH', 'Car Wash & Detailing'),
        ('FULL_SERVICE', 'Full Service'),
        ('REPAIR', 'Repair'),
        ('INSPECTION', 'Inspection'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    tracking_id = models.CharField(max_length=12, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = 'SS' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} - {self.customer.name}"


class WorkAssignment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='assignments')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task_description = models.TextField()
    assigned_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.worker.name} - {self.service_request.tracking_id}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('ONLINE', 'Online Payment'),
        ('OFFLINE', 'Offline / Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=50, blank=True)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = 'RCP' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_number} - ₹{self.amount}"


class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.customer.name}"
