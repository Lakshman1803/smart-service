from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal

from .models import Booking, Vehicle, TimeSlot, ServiceRecord, WorkAssignment, RepairIssue, RepairCharge
from core.models import ServiceCenter, ServiceType
from accounts.models import OTPVerification, Employee, Notification
from accounts.views import send_otp


def send_notification(user, title, message, notif_type='general'):
    Notification.objects.create(user=user, title=title, message=message, notification_type=notif_type)
    print(f"[SMS] → {user.mobile_number}: {message[:100]}")


# ─────────────────────────────────────────────────────────────────────
# CUSTOMER BOOKING FLOW
# ─────────────────────────────────────────────────────────────────────

@login_required
def book_slot_step1(request):
    centers = ServiceCenter.objects.filter(is_active=True).order_by('city')
    return render(request, 'bookings/book_step1.html', {'centers': centers})


@login_required
def book_slot_step2(request):
    if request.method == 'POST':
        center_id    = request.POST.get('service_center')
        date_str     = request.POST.get('date')
        booking_type = request.POST.get('booking_type', 'online')
        vehicle_type = request.POST.get('vehicle_type_filter', 'all')

        request.session['bk_center'] = center_id
        request.session['bk_date']   = date_str
        request.session['bk_type']   = booking_type
        request.session['bk_vtype']  = vehicle_type

        from datetime import datetime
        center = get_object_or_404(ServiceCenter, pk=center_id)
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        slots    = TimeSlot.objects.filter(service_center=center, date=selected_date, is_available=True).order_by('start_time')
        services = ServiceType.objects.filter(is_active=True)
        vehicles = Vehicle.objects.filter(owner=request.user)
        repair_issues = RepairIssue.objects.filter(is_active=True).order_by('vehicle_type', 'category', 'display_order')

        return render(request, 'bookings/book_step2.html', {
            'center': center, 'date': date_str, 'slots': slots,
            'services': services, 'vehicles': vehicles,
            'repair_issues': repair_issues, 'booking_type': booking_type,
        })
    return redirect('book_step1')


@login_required
def book_slot_step3(request):
    if request.method != 'POST':
        return redirect('book_step2')

    slot_id     = request.POST.get('time_slot', '')
    issue_ids   = request.POST.getlist('selected_issues')
    service_ids = request.POST.getlist('services')
    vehicle_id  = request.POST.get('vehicle', '')
    new_vnum    = request.POST.get('new_vehicle', '').strip().upper()
    problem     = request.POST.get('problem_description', '')

    request.session['bk_slot']     = slot_id
    request.session['bk_issues']   = issue_ids
    request.session['bk_services'] = service_ids
    request.session['bk_vehicle']  = vehicle_id
    request.session['bk_new_vnum'] = new_vnum
    request.session['bk_problem']  = problem

    center   = get_object_or_404(ServiceCenter, pk=request.session['bk_center'])
    slot     = TimeSlot.objects.filter(pk=slot_id).first() if slot_id else None
    issues   = RepairIssue.objects.filter(pk__in=issue_ids)
    services = ServiceType.objects.filter(pk__in=service_ids)

    issue_estimate   = sum(i.estimated_cost_max for i in issues)
    service_estimate = sum(s.base_price for s in services)

    return render(request, 'bookings/book_step3.html', {
        'center': center,
        'date': request.session['bk_date'],
        'slot': slot,
        'issues': issues,
        'services': services,
        'issue_estimate': issue_estimate,
        'service_estimate': service_estimate,
        'total_estimate': issue_estimate + service_estimate,
        'problem': problem,
        'steps_data': [
            ('Center & Date', True),
            ('Issues & Services', True),
            ('Review & Confirm', False),
        ],
    })


@login_required
def confirm_booking(request):
    if request.method != 'POST':
        return redirect('book_step1')

    from datetime import datetime
    center_id   = request.session.get('bk_center')
    date_str    = request.session.get('bk_date')
    slot_id     = request.session.get('bk_slot')
    issue_ids   = request.session.get('bk_issues', [])
    service_ids = request.session.get('bk_services', [])
    vehicle_id  = request.session.get('bk_vehicle', '')
    new_vnum    = request.session.get('bk_new_vnum', '')
    problem     = request.session.get('bk_problem', '')
    bk_type     = request.session.get('bk_type', 'online')

    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    center = get_object_or_404(ServiceCenter, pk=center_id)

    # Resolve vehicle
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)
    elif new_vnum:
        vehicle, _ = Vehicle.objects.get_or_create(
            vehicle_number=new_vnum,
            defaults={'owner': request.user, 'make': 'Unknown', 'model': 'Unknown',
                      'year': 2020, 'vehicle_type': '4w'}
        )
    else:
        messages.error(request, 'Please select or enter a vehicle number.')
        return redirect('book_step2')

    slot         = TimeSlot.objects.filter(pk=slot_id).first() if slot_id else None
    booking_time = slot.start_time if slot else timezone.now().time()

    booking = Booking.objects.create(
        customer=request.user, vehicle=vehicle, service_center=center,
        time_slot=slot, booking_type=bk_type,
        booking_date=selected_date, booking_time=booking_time,
        problem_description=problem, status='confirmed',
    )
    booking.service_types.set(service_ids)
    booking.selected_issues.set(issue_ids)

    # Create RepairCharge rows from selected issues
    for issue in RepairIssue.objects.filter(pk__in=issue_ids):
        RepairCharge.objects.create(
            booking=booking, repair_issue=issue, charge_type='selected',
            description=issue.name, quantity=1,
            unit_price=issue.estimated_cost_max, is_extra=False,
        )
    # Create RepairCharge rows from service types
    for stype in ServiceType.objects.filter(pk__in=service_ids):
        RepairCharge.objects.create(
            booking=booking, charge_type='service',
            description=stype.name, quantity=1, unit_price=stype.base_price,
        )

    booking.calculate_estimate()

    if slot:
        slot.current_bookings += 1
        if slot.current_bookings >= slot.max_bookings:
            slot.is_available = False
        slot.save()

    send_notification(
        request.user, 'Booking Confirmed ✅',
        f'Booking {booking.booking_id} at {center.name} on {date_str} confirmed. Show this ID at the center.',
        'booking_confirm'
    )

    for k in ['bk_center','bk_date','bk_slot','bk_issues','bk_services',
              'bk_vehicle','bk_new_vnum','bk_problem','bk_type','bk_vtype']:
        request.session.pop(k, None)

    messages.success(request, f'Booking confirmed! ID: {booking.booking_id}')
    return redirect('booking_detail', pk=booking.pk)


# ─────────────────────────────────────────────────────────────────────
# CUSTOMER — view bookings
# ─────────────────────────────────────────────────────────────────────

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    charges = RepairCharge.objects.filter(booking=booking)
    return render(request, 'bookings/booking_detail.html', {'booking': booking, 'charges': charges})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('my_bookings')


# ─────────────────────────────────────────────────────────────────────
# EMPLOYEE — manage bookings
# ─────────────────────────────────────────────────────────────────────

@login_required
def employee_bookings(request):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    try:
        emp = request.user.employee_profile
        qs  = Booking.objects.filter(service_center=emp.service_center)
    except Exception:
        qs  = Booking.objects.all() if request.user.role == 'admin' else Booking.objects.none()

    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'bookings/employee_bookings.html', {
        'bookings': qs.order_by('-created_at'), 'status_filter': status_filter,
    })


@login_required
def employee_booking_detail(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking    = get_object_or_404(Booking, pk=pk)
    charges    = RepairCharge.objects.filter(booking=booking)
    workers    = Employee.objects.filter(service_center=booking.service_center, is_active=True)
    all_issues = RepairIssue.objects.filter(is_active=True)
    return render(request, 'bookings/employee_booking_detail.html', {
        'booking': booking, 'charges': charges,
        'workers': workers, 'all_issues': all_issues,
    })


@login_required
def add_extra_charge(request, pk):
    """Employee adds an extra/diagnosed/parts/labour charge."""
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        desc        = request.POST.get('description', '').strip()
        qty         = Decimal(request.POST.get('quantity', '1') or '1')
        unit_price  = Decimal(request.POST.get('unit_price', '0') or '0')
        charge_type = request.POST.get('charge_type', 'extra')
        issue_id    = request.POST.get('repair_issue', '')

        if desc and unit_price > 0:
            emp      = getattr(request.user, 'employee_profile', None)
            issue_obj = RepairIssue.objects.filter(pk=issue_id).first() if issue_id else None
            RepairCharge.objects.create(
                booking=booking, repair_issue=issue_obj,
                charge_type=charge_type, description=desc,
                quantity=qty, unit_price=unit_price,
                is_extra=(charge_type == 'extra'), added_by=emp,
            )
            messages.success(request, f'Charge added: {desc} — ₹{float(qty*unit_price):.2f}')
        else:
            messages.error(request, 'Fill in description and unit price.')

    return redirect('employee_booking_detail', pk=pk)


@login_required
def remove_charge(request, charge_pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    charge = get_object_or_404(RepairCharge, pk=charge_pk)
    booking_pk = charge.booking.pk
    charge.delete()
    messages.success(request, 'Charge removed.')
    return redirect('employee_booking_detail', pk=booking_pk)


@login_required
def verify_customer_otp(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'send_otp':
            otp_obj = OTPVerification.generate_otp(booking.customer.mobile_number, purpose='service_accept')
            send_otp(booking.customer.mobile_number, otp_obj.otp, 'service_accept')
            messages.info(request, f'OTP sent to ...{booking.customer.mobile_number[-4:]}')
            return render(request, 'bookings/verify_customer_otp.html', {'booking': booking, 'otp_sent': True})
        elif action == 'verify_otp':
            otp_entered = request.POST.get('otp', '').strip()
            otp_obj     = OTPVerification.objects.filter(
                mobile_number=booking.customer.mobile_number,
                otp=otp_entered, purpose='service_accept', is_used=False
            ).first()
            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True; otp_obj.save()
                booking.otp_verified = True
                booking.status       = 'in_progress'
                booking.check_in_time = timezone.now()
                booking.save()
                messages.success(request, 'OTP verified! Service started.')
                return redirect('employee_booking_detail', pk=pk)
            else:
                messages.error(request, 'Invalid or expired OTP.')

    return render(request, 'bookings/verify_customer_otp.html', {'booking': booking})


@login_required
def add_customer_vehicle(request):
    """Employee creates a walk-in booking with issue selection."""
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')

    if request.method == 'POST':
        mobile      = request.POST.get('customer_mobile', '').strip()
        cname       = request.POST.get('customer_name', 'Customer').strip()
        veh_num     = request.POST.get('vehicle_number', '').strip().upper()
        make        = request.POST.get('make', 'Unknown')
        model       = request.POST.get('model', 'Unknown')
        year        = int(request.POST.get('year', 2020) or 2020)
        v_type      = request.POST.get('vehicle_type', '4w')
        fuel        = request.POST.get('fuel_type', 'petrol')
        km          = int(request.POST.get('current_km', 0) or 0)
        problem     = request.POST.get('problem_description', '')
        center_id   = request.POST.get('service_center')
        service_ids = request.POST.getlist('services')
        issue_ids   = request.POST.getlist('selected_issues')

        from accounts.models import User
        fname = cname.split()[0] if cname else 'Customer'
        lname = ' '.join(cname.split()[1:]) if len(cname.split()) > 1 else ''
        customer, _ = User.objects.get_or_create(
            mobile_number=mobile,
            defaults={'role': 'customer', 'first_name': fname, 'last_name': lname}
        )
        vehicle, _ = Vehicle.objects.get_or_create(
            vehicle_number=veh_num,
            defaults={'owner': customer, 'make': make, 'model': model,
                      'year': year, 'vehicle_type': v_type,
                      'fuel_type': fuel, 'current_km': km}
        )
        center  = get_object_or_404(ServiceCenter, pk=center_id)
        booking = Booking.objects.create(
            customer=customer, vehicle=vehicle, service_center=center,
            booking_type='offline', booking_date=timezone.now().date(),
            booking_time=timezone.now().time(), problem_description=problem,
            status='confirmed',
        )
        booking.service_types.set(service_ids)
        booking.selected_issues.set(issue_ids)

        for issue in RepairIssue.objects.filter(pk__in=issue_ids):
            RepairCharge.objects.create(
                booking=booking, repair_issue=issue, charge_type='selected',
                description=issue.name, quantity=1,
                unit_price=issue.estimated_cost_max, is_extra=False,
            )
        for stype in ServiceType.objects.filter(pk__in=service_ids):
            RepairCharge.objects.create(
                booking=booking, charge_type='service',
                description=stype.name, quantity=1, unit_price=stype.base_price,
            )
        booking.calculate_estimate()

        messages.success(request, f'Walk-in booking {booking.booking_id} created.')
        return redirect('employee_booking_detail', pk=booking.pk)

    centers       = ServiceCenter.objects.filter(is_active=True)
    services      = ServiceType.objects.filter(is_active=True)
    repair_issues = RepairIssue.objects.filter(is_active=True).order_by('vehicle_type','category','display_order')
    return render(request, 'bookings/add_customer_vehicle.html', {
        'centers': centers, 'services': services, 'repair_issues': repair_issues,
    })


@login_required
def assign_workers(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        worker_ids = request.POST.getlist('workers')
        task       = request.POST.get('task_description', '')
        booking.assigned_workers.set(worker_ids)
        WorkAssignment.objects.filter(booking=booking).delete()
        for wid in worker_ids:
            WorkAssignment.objects.create(booking=booking, worker_id=wid, task_description=task)
        try:
            booking.assigned_employee = request.user.employee_profile
            booking.save()
        except Exception:
            pass
        messages.success(request, 'Workers assigned.')
        return redirect('employee_booking_detail', pk=pk)
    workers = Employee.objects.filter(service_center=booking.service_center, is_active=True)
    return render(request, 'bookings/assign_workers.html', {'booking': booking, 'workers': workers})


@login_required
def complete_service(request, pk):
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        ServiceRecord.objects.update_or_create(
            booking=booking,
            defaults={
                'vehicle': booking.vehicle,
                'employee': getattr(request.user, 'employee_profile', None),
                'work_done':      request.POST.get('work_done', ''),
                'parts_replaced': request.POST.get('parts_replaced', ''),
                'next_service_km': request.POST.get('next_service_km') or None,
                'technician_notes': request.POST.get('technician_notes', ''),
                'completed_at':   timezone.now(),
            }
        )
        booking.status       = 'completed'
        booking.completed_at = timezone.now()
        booking.save()
        send_notification(
            booking.customer, '🎉 Service Completed!',
            f'Vehicle {booking.vehicle.vehicle_number} service done at {booking.service_center.name}. '
            f'Booking: {booking.booking_id}',
            'service_complete'
        )
        messages.success(request, 'Service completed! Customer notified.')
        return redirect('create_bill', pk=pk)
    return render(request, 'bookings/complete_service.html', {'booking': booking})


def get_available_slots(request):
    cid   = request.GET.get('center_id')
    date  = request.GET.get('date')
    if cid and date:
        slots = TimeSlot.objects.filter(
            service_center_id=cid, date=date, is_available=True
        ).values('id', 'start_time', 'end_time', 'slots_remaining')
        return JsonResponse({'slots': list(slots)})
    return JsonResponse({'slots': []})


@login_required
def update_charge_price(request, charge_pk):
    """Employee updates the unit price of an existing charge."""
    if request.user.role not in ['employee', 'admin']:
        return redirect('home')
    charge = get_object_or_404(RepairCharge, pk=charge_pk)
    if request.method == 'POST':
        try:
            from decimal import Decimal
            new_price = Decimal(request.POST.get('unit_price', str(charge.unit_price)))
            if new_price >= 0:
                charge.unit_price = new_price
                charge.save()
                messages.success(request, f'Price updated to ₹{new_price:.2f}')
            else:
                messages.error(request, 'Price cannot be negative.')
        except Exception:
            messages.error(request, 'Invalid price value.')
    return redirect('create_bill', pk=charge.booking.pk)
