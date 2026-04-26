from django.db import models
from django.utils import timezone


class ServiceCenter(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('TS', 'Telangana'),
    ]

    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=5, choices=STATE_CHOICES, default='AP')
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    google_maps_link = models.URLField(blank=True)
    working_days = models.CharField(max_length=100, default='Monday to Saturday')
    working_hours = models.CharField(max_length=100, default='8:00 AM - 7:00 PM')
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='service_centers/', blank=True, null=True)
    manager_name = models.CharField(max_length=100, blank=True)
    total_bays = models.IntegerField(default=10)
    established_year = models.IntegerField(null=True, blank=True)
    # Payment QR code uploaded by admin/employee
    payment_qr_code = models.ImageField(
        upload_to='payment_qr/', blank=True, null=True,
        help_text='Upload UPI QR code image for this service center'
    )
    upi_id = models.CharField(
        max_length=100, blank=True, default='smartrepair@upi',
        help_text='UPI ID e.g. smartrepair.vjw@upi'
    )

    class Meta:
        ordering = ['city', 'name']

    def __str__(self):
        return f"{self.name} - {self.city}"

    @property
    def coordinates(self):
        if self.latitude and self.longitude:
            return f"{self.latitude},{self.longitude}"
        return None


class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)
    is_national = models.BooleanField(default=False)
    service_centers = models.ManyToManyField(ServiceCenter, blank=True, help_text='Leave empty for all centers')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} - {self.date}"

    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()


class ServiceType(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('2w', 'Two Wheeler'),
        ('3w', 'Three Wheeler'),
        ('4w', 'Four Wheeler'),
        ('heavy', 'Heavy Vehicle'),
        ('all', 'All Vehicles'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='all')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.IntegerField(help_text='Duration in hours')
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    reply = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
