from django.db import models
import uuid


def generate_receipt_number():
    return 'RCP' + uuid.uuid4().hex[:8].upper()


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online (UPI/QR)'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    receipt_number = models.CharField(max_length=20, unique=True, default=generate_receipt_number)
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    # ------ Amount breakdown ------
    # 1) Issue charges (from RepairCharge with charge_type='selected'/'diagnosed'/'service')
    issue_charges_total = models.DecimalField(max_digits=12, decimal_places=2, default=0,
        help_text='Total from customer-selected repair issues + service types')
    # 2) Extra charges added by employee after inspection
    extra_charges_total = models.DecimalField(max_digits=12, decimal_places=2, default=0,
        help_text='Total from extra/additional work added by employee')
    # 3) Parts
    parts_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # 4) Labour
    labour_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    upi_reference = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    billed_by = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.receipt_number} — ₹{self.total_amount}"

    def recalculate(self):
        """Recompute all totals from RepairCharge rows linked to this booking."""
        from bookings.models import RepairCharge
        charges = RepairCharge.objects.filter(booking=self.booking)

        issue_types   = ['selected', 'diagnosed', 'service']
        extra_types   = ['extra']
        parts_types   = ['parts']
        labour_types  = ['labour']

        self.issue_charges_total = sum(c.total for c in charges if c.charge_type in issue_types)
        self.extra_charges_total = sum(c.total for c in charges if c.charge_type in extra_types)
        self.parts_total         = sum(c.total for c in charges if c.charge_type in parts_types)
        self.labour_total        = sum(c.total for c in charges if c.charge_type in labour_types)

        self.subtotal   = self.issue_charges_total + self.extra_charges_total + self.parts_total + self.labour_total
        self.gst_amount = (self.subtotal * self.gst_rate) / 100
        self.total_amount = self.subtotal + self.gst_amount - self.discount
        self.save()
        return self.total_amount


# Legacy alias kept for backward compat — new code uses RepairCharge from bookings app
class ServiceCharge(models.Model):
    """Kept for migration compatibility. New billing uses bookings.RepairCharge."""
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='legacy_charges')
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_extra = models.BooleanField(default=False)
    added_by = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} — ₹{self.total}"
