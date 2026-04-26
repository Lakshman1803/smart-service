from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal

from .models import Payment
from bookings.models import Booking, RepairCharge
from accounts.models import Notification
from core.models import ServiceCenter


def _get_employee(user):
    try:
        return user.employee_profile
    except Exception:
        return None


def _build_totals(charges):
    selected = charges.filter(charge_type__in=['selected', 'diagnosed', 'service'])
    extra    = charges.filter(is_extra=True)
    parts    = charges.filter(charge_type='parts')
    labour   = charges.filter(charge_type='labour')

    issue_total  = sum(c.total for c in selected)
    extra_total  = sum(c.total for c in extra)
    parts_total  = sum(c.total for c in parts)
    labour_total = sum(c.total for c in labour)
    subtotal     = issue_total + extra_total + parts_total + labour_total
    gst          = subtotal * Decimal('0.18')
    grand_total  = subtotal + gst

    return {
        'issue_total':      issue_total,
        'extra_total':      extra_total,
        'parts_total':      parts_total,
        'labour_total':     labour_total,
        'subtotal':         subtotal,
        'gst':              gst,
        'grand_total':      grand_total,
        'selected_charges': selected,
        'extra_charges':    extra,
        'parts_charges':    parts,
        'labour_charges':   labour,
    }


@login_required
def create_bill(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)
    charges = RepairCharge.objects.filter(booking=booking).order_by('charge_type', 'added_at')

    if not charges.exists():
        emp = _get_employee(request.user)
        for issue in booking.selected_issues.all():
            RepairCharge.objects.create(
                booking=booking, repair_issue=issue, charge_type='selected',
                description=issue.name, quantity=1,
                unit_price=issue.estimated_cost_min, is_extra=False, added_by=emp,
            )
        for stype in booking.service_types.all():
            RepairCharge.objects.create(
                booking=booking, charge_type='service',
                description=stype.name, quantity=1,
                unit_price=stype.base_price, is_extra=False, added_by=emp,
            )
        charges = RepairCharge.objects.filter(booking=booking).order_by('charge_type', 'added_at')

    totals = _build_totals(charges)
    return render(request, 'payments/create_bill.html', {
        'booking': booking, 'charges': charges, **totals,
    })


@login_required
def finalize_payment(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking  = get_object_or_404(Booking, pk=pk)
    charges  = RepairCharge.objects.filter(booking=booking)
    totals   = _build_totals(charges)
    discount = Decimal(request.POST.get('discount', '0') or '0')
    method   = request.POST.get('payment_method', 'cash')
    notes    = request.POST.get('notes', '')
    final    = totals['grand_total'] - discount

    payment, _ = Payment.objects.update_or_create(
        booking=booking,
        defaults={
            'customer':            booking.customer,
            'issue_charges_total': totals['issue_total'],
            'extra_charges_total': totals['extra_total'],
            'parts_total':         totals['parts_total'],
            'labour_total':        totals['labour_total'],
            'subtotal':            totals['subtotal'],
            'gst_amount':          totals['gst'],
            'discount':            discount,
            'total_amount':        final,
            'payment_method':      method,
            'payment_status':      'paid',
            'paid_at':             timezone.now(),
            'billed_by':           _get_employee(request.user),
            'notes':               notes,
        }
    )
    Notification.objects.create(
        user=booking.customer,
        title='💳 Payment Receipt Ready',
        message=f'Payment ₹{final:.2f} recorded for {booking.booking_id} via {method.upper()}. Receipt: {payment.receipt_number}',
        notification_type='payment'
    )
    messages.success(request, f'Payment ₹{final:.2f} finalised. Receipt: {payment.receipt_number}')
    return redirect('view_receipt', pk=payment.pk)


@login_required
def view_receipt(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.user != payment.customer and request.user.role not in ['employee', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    booking = payment.booking
    charges = RepairCharge.objects.filter(booking=booking).order_by('charge_type', 'added_at')
    totals  = _build_totals(charges)
    return render(request, 'payments/receipt.html', {
        'payment': payment, 'booking': booking, 'charges': charges, **totals,
    })


# ──────────────────────────────────────────────────────────────────────
# ONLINE PAYMENT — Shows service center's uploaded QR code
# ──────────────────────────────────────────────────────────────────────
@login_required
def online_payment(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user != booking.customer and request.user.role not in ['employee', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    charges = RepairCharge.objects.filter(booking=booking)
    if not charges.exists():
        messages.warning(request, 'No charges added yet. Please check with service center.')
        return redirect('booking_detail', pk=pk)

    totals = _build_totals(charges)
    center = booking.service_center

    return render(request, 'payments/online_payment.html', {
        'booking': booking,
        'center': center,
        **totals,
    })


@login_required
@require_POST
def confirm_online_payment(request, pk):
    """
    AJAX endpoint — called after customer confirms payment on the QR page.
    Creates/updates the Payment record and returns JSON with receipt URL.
    """
    booking = get_object_or_404(Booking, pk=pk)
    if request.user != booking.customer and request.user.role not in ['employee', 'admin']:
        return JsonResponse({'success': False, 'error': 'Access denied.'}, status=403)

    charges  = RepairCharge.objects.filter(booking=booking)
    totals   = _build_totals(charges)
    upi_ref  = request.POST.get('upi_reference', '').strip()
    discount = Decimal(request.POST.get('discount', '0') or '0')
    final    = totals['grand_total'] - discount

    if not upi_ref:
        return JsonResponse({'success': False, 'error': 'Please enter the UPI transaction reference number.'})

    payment, _ = Payment.objects.update_or_create(
        booking=booking,
        defaults={
            'customer':            booking.customer,
            'issue_charges_total': totals['issue_total'],
            'extra_charges_total': totals['extra_total'],
            'parts_total':         totals['parts_total'],
            'labour_total':        totals['labour_total'],
            'subtotal':            totals['subtotal'],
            'gst_amount':          totals['gst'],
            'discount':            discount,
            'total_amount':        final,
            'payment_method':      'online',
            'upi_reference':       upi_ref,
            'payment_status':      'paid',
            'paid_at':             timezone.now(),
        }
    )
    Notification.objects.create(
        user=booking.customer,
        title='✅ Online Payment Confirmed',
        message=(f'UPI payment ₹{final:.2f} confirmed for booking {booking.booking_id}. '
                 f'UTR: {upi_ref}. Receipt: {payment.receipt_number}'),
        notification_type='payment'
    )

    from django.urls import reverse
    receipt_url = reverse('view_receipt', kwargs={'pk': payment.pk})
    return JsonResponse({
        'success':        True,
        'receipt_url':    receipt_url,
        'receipt_number': payment.receipt_number,
        'total':          str(final),
        'booking_id':     booking.booking_id,
    })


# ──────────────────────────────────────────────────────────────────────
# EMPLOYEE — Upload/Update QR code for their service center
# ──────────────────────────────────────────────────────────────────────
@login_required
def upload_qr_code(request):
    if request.user.role not in ['employee', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    emp = _get_employee(request.user)
    center = emp.service_center if emp else None

    # Admin can select any center
    if request.user.role == 'admin' and request.GET.get('center'):
        center = get_object_or_404(ServiceCenter, pk=request.GET.get('center'))

    if request.method == 'POST':
        center_pk = request.POST.get('center_pk')
        if center_pk:
            center = get_object_or_404(ServiceCenter, pk=center_pk)

        upi_id = request.POST.get('upi_id', '').strip()
        qr_file = request.FILES.get('payment_qr_code')

        if upi_id:
            center.upi_id = upi_id
        if qr_file:
            # Delete old QR if exists
            if center.payment_qr_code:
                try:
                    import os
                    if os.path.exists(center.payment_qr_code.path):
                        os.remove(center.payment_qr_code.path)
                except Exception:
                    pass
            center.payment_qr_code = qr_file

        center.save()
        messages.success(request, f'✅ Payment QR code updated for {center.name}!')
        return redirect('upload_qr_code')

    # Admin sees all centers
    all_centers = ServiceCenter.objects.filter(is_active=True).order_by('city') if request.user.role == 'admin' else None

    return render(request, 'payments/upload_qr.html', {
        'center': center,
        'all_centers': all_centers,
    })


@login_required
def my_payments(request):
    payments = Payment.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'payments/my_payments.html', {'payments': payments})
