from django.db import models
from django.utils import timezone
import uuid


def generate_booking_id():
    return 'SR' + uuid.uuid4().hex[:8].upper()


class RepairIssue(models.Model):
    """Predefined repair issues customers select while booking"""
    """Predefined repair issues customers select while booking — shown with price range"""
    VEHICLE_TYPE_CHOICES = [
        ('2w', 'Two Wheeler'), ('3w', 'Three Wheeler'),
        ('4w', 'Four Wheeler'), ('heavy', 'Heavy Vehicle'), ('all', 'All Vehicles'),
    ]
    CATEGORY_CHOICES = [
        ('engine', 'Engine'), ('brakes', 'Brakes & Suspension'),
        ('electrical', 'Electrical'), ('tyres', 'Tyres & Wheels'),
        ('ac', 'AC & Cooling'), ('body', 'Body & Paint'),
        ('transmission', 'Transmission & Clutch'), ('fuel', 'Fuel System'),
        ('service', 'Periodic Service'), ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='all')
    estimated_cost_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_cost_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['vehicle_type', 'category', 'display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"

    @property
    def cost_range(self):
        if self.estimated_cost_min == self.estimated_cost_max:
            return f"₹{int(self.estimated_cost_min):,}"
        return f"₹{int(self.estimated_cost_min):,} – ₹{int(self.estimated_cost_max):,}"

    @property
    def avg_cost(self):
        return (self.estimated_cost_min + self.estimated_cost_max) / 2


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('2w', 'Two Wheeler'), ('3w', 'Three Wheeler'),
        ('4w', 'Four Wheeler'), ('heavy', 'Heavy Vehicle'),
    ]
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'), ('diesel', 'Diesel'),
        ('electric', 'Electric'), ('cng', 'CNG'), ('hybrid', 'Hybrid'),
    ]
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='petrol')
    color = models.CharField(max_length=50, blank=True)
    chassis_number = models.CharField(max_length=50, blank=True)
    engine_number = models.CharField(max_length=50, blank=True)
    current_km = models.IntegerField(default=0)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.make} {self.model}"


class TimeSlot(models.Model):
    service_center = models.ForeignKey('core.ServiceCenter', on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_bookings = models.IntegerField(default=5)
    current_bookings = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['service_center', 'date', 'start_time']

    def __str__(self):
        return f"{self.service_center.city} - {self.date} {self.start_time}"

    @property
    def is_full(self):
        return self.current_bookings >= self.max_bookings

    @property
    def slots_remaining(self):
        return self.max_bookings - self.current_bookings


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [('online', 'Online'), ('offline', 'Offline/Walk-in')]
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, default=generate_booking_id)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    service_center = models.ForeignKey('core.ServiceCenter', on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    service_types = models.ManyToManyField('core.ServiceType', blank=True)
    # Customer-selected repair issues at booking time
    selected_issues = models.ManyToManyField(RepairIssue, blank=True, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='online')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    problem_description = models.TextField(blank=True)
    issue_notes = models.TextField(blank=True, help_text='Additional notes about the issues')
    assigned_employee = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    assigned_workers = models.ManyToManyField('accounts.Employee', blank=True, related_name='worker_bookings')
    otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    customer_km_reading = models.IntegerField(null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    distance_from_center = models.FloatField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_id} - {self.customer.get_full_name()} - {self.status}"

    def calculate_estimate(self):
        """Sum selected repair issue max costs + service type prices"""
        issue_total = sum(i.estimated_cost_max for i in self.selected_issues.all())
        service_total = sum(s.base_price for s in self.service_types.all())
        self.estimated_total = issue_total + service_total
        self.save(update_fields=['estimated_total'])
        return self.estimated_total


class RepairCharge(models.Model):
    """Actual charges against a booking — base (from selected issues) + extra added by employee"""
    CHARGE_TYPE_CHOICES = [
        ('selected', 'Customer Selected Issue'),
        ('diagnosed', 'Diagnosed at Center'),
        ('parts', 'Parts & Materials'),
        ('labour', 'Labour Charges'),
        ('extra', 'Extra / Additional Work'),
        ('service', 'Service Charge'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='repair_charges')
    repair_issue = models.ForeignKey(RepairIssue, on_delete=models.SET_NULL, null=True, blank=True)
    charge_type = models.CharField(max_length=20, choices=CHARGE_TYPE_CHOICES, default='service')
    description = models.CharField(max_length=300)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_extra = models.BooleanField(default=False, help_text='Extra work added after inspection')
    added_by = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['charge_type', 'added_at']

    def __str__(self):
        return f"{self.description} — ₹{self.total}"

    @property
    def total(self):
        return self.quantity * self.unit_price


class ServiceRecord(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='service_record')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    employee = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, related_name='service_records')
    diagnosis = models.TextField(blank=True)
    work_done = models.TextField()
    parts_replaced = models.TextField(blank=True)
    next_service_km = models.IntegerField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    technician_notes = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    km_reading = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Service Record - {self.booking.booking_id}"


class WorkAssignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='work_assignments')
    worker = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='work_assignments')
    task_description = models.TextField()
    assigned_issues = models.ManyToManyField(RepairIssue, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Work: {self.worker.user.get_full_name()} - {self.booking.booking_id}"
