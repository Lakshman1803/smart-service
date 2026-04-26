from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
import string


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('Mobile number is required')
        user = self.model(mobile_number=mobile_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(mobile_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    ]

    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name() or self.mobile_number} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ('manager', 'Manager'),
        ('mechanic', 'Mechanic'),
        ('electrician', 'Electrician'),
        ('painter', 'Painter'),
        ('supervisor', 'Supervisor'),
        ('receptionist', 'Receptionist'),
        ('worker', 'Worker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    service_center = models.ForeignKey('core.ServiceCenter', on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"


class OTPVerification(models.Model):
    PURPOSE_CHOICES = [
        ('login', 'Login'),
        ('register', 'Register'),
        ('service_accept', 'Service Acceptance'),
        ('payment', 'Payment'),
    ]

    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default='login')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    @classmethod
    def generate_otp(cls, mobile_number, purpose='login'):
        otp = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        cls.objects.filter(mobile_number=mobile_number, purpose=purpose, is_used=False).update(is_used=True)
        return cls.objects.create(
            mobile_number=mobile_number,
            otp=otp,
            purpose=purpose,
            expires_at=expires_at
        )

    def __str__(self):
        return f"OTP for {self.mobile_number} - {self.purpose}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('service_complete', 'Service Completed'),
        ('booking_confirm', 'Booking Confirmed'),
        ('reminder', 'Service Reminder'),
        ('payment', 'Payment'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.mobile_number}"
