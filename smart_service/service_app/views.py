from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import (Customer, Employee, Vehicle, ServiceRequest, WorkAssignment,
                     Worker, Payment, Notification, OTP)
from .utils import generate_otp, send_otp, verify_otp
import json
from decimal import Decimal


# ─── Public Views ──────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'service_app/home.html')


def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! We'll contact you shortly.")
        return redirect('contact')
    return render(request, 'service_app/contact.html')


def track_service(request):
    tracking_id = request.GET.get('tracking_id', '').strip().upper()
    service = None
    error = None
    if tracking_id:
        try:
            service = ServiceRequest.objects.select_related('customer', 'vehicle', 'employee').prefetch_related('assignments__worker').get(tracking_id=tracking_id)
        except ServiceRequest.DoesNotExist:
            error = "No service found with this tracking ID."
    return render(request, 'service_app/track.html', {'service': service, 'tracking_id': tracking_id, 'error': error})


def service_detail(request, tracking_id):
    service = get_object_or_404(ServiceRequest, tracking_id=tracking_id.upper())
    return render(request, 'service_app/service_detail.html', {'service': service})


def custom_404(request, exception):
    return render(request, 'service_app/404.html', status=404)


# ─── Customer Auth ─────────────────────────────────────────────────────────────

def customer_login(request):
    if request.session.get('customer_id'):
        return redirect('customer_dashboard')
    return render(request, 'service_app/customer_login.html')


def send_customer_otp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile', '').strip()
        if len(mobile) != 10 or not mobile.isdigit():
            messages.error(request, "Enter a valid 10-digit mobile number.")
            return redirect('customer_login')
        otp_code = generate_otp(mobile, 'customer_login')
        send_otp(mobile, otp_code, 'login')
        request.session['otp_mobile'] = mobile
        messages.success(request, f"OTP sent to {mobile[:3]}*****{mobile[-2:]} (check console if dev mode)")
        return render(request, 'service_app/otp_verify.html', {'mobile': mobile, 'purpose': 'customer_login'})
    return redirect('customer_login')


def verify_customer_otp(request):
    if request.method == 'POST':
        mobile = request.session.get('otp_mobile')
        otp_code = request.POST.get('otp', '').strip()
        purpose = request.POST.get('purpose', 'customer_login')
        if not mobile:
            messages.error(request, "Session expired. Please try again.")
            return redirect('customer_login')
        if verify_otp(mobile, otp_code, purpose):
            customer, created = Customer.objects.get_or_create(mobile=mobile, defaults={'name': 'Customer'})
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.name
            del request.session['otp_mobile']
            if created or customer.name == 'Customer':
                messages.info(request, "Welcome! Please complete your profile.")
                return redirect('customer_register')
            messages.success(request, f"Welcome back, {customer.name}!")
            return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            return render(request, 'service_app/otp_verify.html', {'mobile': mobile, 'purpose': purpose})
    return redirect('customer_login')


def customer_register(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.name = request.POST.get('name', '').strip()
        customer.email = request.POST.get('email', '').strip()
        customer.address = request.POST.get('address', '').strip()
        customer.save()
        request.session['customer_name'] = customer.name
        messages.success(request, "Profile updated successfully!")
        return redirect('customer_dashboard')
    return render(request, 'service_app/customer_register.html', {'customer': customer})


def customer_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('home')


def customer_dashboard(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, "Please login first.")
        return redirect('customer_login')
    customer = get_object_or_404(Customer, id=customer_id)
    services = ServiceRequest.objects.filter(customer=customer).order_by('-created_at')
    notifications = Notification.objects.filter(customer=customer, is_read=False).order_by('-created_at')
    notifications.update(is_read=True)
    return render(request, 'service_app/customer_dashboard.html', {
        'customer': customer, 'services': services, 'notifications': notifications
    })


# ─── Employee Auth ─────────────────────────────────────────────────────────────

def employee_login(request):
    if request.session.get('employee_id'):
        return redirect('employee_dashboard')
    if request.method == 'POST':
        emp_id = request.POST.get('employee_id', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        try:
            employee = Employee.objects.get(employee_id=emp_id, mobile=mobile, is_active=True)
            request.session['employee_id'] = employee.id
            request.session['employee_name'] = employee.name
            request.session['employee_role'] = employee.role
            messages.success(request, f"Welcome, {employee.name}!")
            return redirect('employee_dashboard')
        except Employee.DoesNotExist:
            messages.error(request, "Invalid Employee ID or Mobile Number. Please check credentials.")
            return render(request, 'service_app/employee_login.html', {'error': True})
    return render(request, 'service_app/employee_login.html')


def employee_logout(request):
    for key in ['employee_id', 'employee_name', 'employee_role']:
        request.session.pop(key, None)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('employee_id'):
            messages.error(request, "Please login as employee first.")
            return redirect('employee_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Employee Dashboard ─────────────────────────────────────────────────────────

@employee_required
def employee_dashboard(request):
    employee = get_object_or_404(Employee, id=request.session['employee_id'])
    services = ServiceRequest.objects.select_related('customer', 'vehicle').order_by('-created_at')[:20]
    workers = Worker.objects.all()
    return render(request, 'service_app/employee_dashboard.html', {
        'employee': employee, 'services': services, 'workers': workers
    })


@employee_required
def add_service_request(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        vehicle_number = request.POST.get('vehicle_number', '').strip().upper()
        vehicle_type = request.POST.get('vehicle_type', '')
        brand = request.POST.get('brand', '').strip()
        model = request.POST.get('model_name', '').strip()
        service_type = request.POST.get('service_type', '')
        description = request.POST.get('description', '').strip()
        estimated_amount = request.POST.get('estimated_amount', 0)

        if len(mobile) != 10:
            messages.error(request, "Invalid mobile number.")
            return redirect('add_service_request')

        customer, _ = Customer.objects.get_or_create(mobile=mobile, defaults={'name': name})
        if customer.name == 'Customer' or not customer.name:
            customer.name = name
            customer.save()

        vehicle, _ = Vehicle.objects.get_or_create(
            vehicle_number=vehicle_number,
            defaults={'customer': customer, 'vehicle_type': vehicle_type, 'brand': brand, 'model': model}
        )

        employee = get_object_or_404(Employee, id=request.session['employee_id'])
        service = ServiceRequest.objects.create(
            customer=customer, vehicle=vehicle, employee=employee,
            service_type=service_type, description=description,
            estimated_amount=estimated_amount, status='PENDING'
        )

        # Send OTP to customer for verification
        otp_code = generate_otp(mobile, 'verify_vehicle')
        send_otp(mobile, otp_code, 'service acceptance')
        request.session['pending_service_id'] = service.id
        request.session['verify_mobile'] = mobile

        messages.info(request, f"OTP sent to customer {mobile[:3]}*****{mobile[-2:]} for service acceptance.")
        return render(request, 'service_app/otp_verify.html', {
            'mobile': mobile, 'purpose': 'verify_vehicle',
            'service': service, 'employee_mode': True
        })

    return render(request, 'service_app/add_service.html', {
        'service_types': ServiceRequest.SERVICE_TYPES,
        'vehicle_types': Vehicle.VEHICLE_TYPES,
    })


def send_vehicle_otp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile', '').strip()
        otp_code = generate_otp(mobile, 'verify_vehicle')
        send_otp(mobile, otp_code, 'service acceptance')
        return JsonResponse({'status': 'sent'})
    return JsonResponse({'status': 'error'}, status=400)


@employee_required
def verify_vehicle_otp(request):
    if request.method == 'POST':
        mobile = request.session.get('verify_mobile')
        otp_code = request.POST.get('otp', '').strip()
        service_id = request.session.get('pending_service_id')
        if verify_otp(mobile, otp_code, 'verify_vehicle'):
            service = get_object_or_404(ServiceRequest, id=service_id)
            service.status = 'ACCEPTED'
            service.save()
            # Notify customer
            Notification.objects.create(
                customer=service.customer,
                message=f"Your service request #{service.tracking_id} has been accepted. We'll keep you updated."
            )
            del request.session['pending_service_id']
            del request.session['verify_mobile']
            messages.success(request, f"Service #{service.tracking_id} accepted after OTP verification!")
            return redirect('assign_work', service_id=service.id)
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            service = get_object_or_404(ServiceRequest, id=service_id)
            return render(request, 'service_app/otp_verify.html', {
                'mobile': mobile, 'purpose': 'verify_vehicle',
                'service': service, 'employee_mode': True
            })
    return redirect('employee_dashboard')


@employee_required
def assign_work(request, service_id):
    service = get_object_or_404(ServiceRequest, id=service_id)
    workers = Worker.objects.all()
    assignments = WorkAssignment.objects.filter(service_request=service).select_related('worker')
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        task = request.POST.get('task_description', '').strip()
        worker = get_object_or_404(Worker, id=worker_id)
        employee = get_object_or_404(Employee, id=request.session['employee_id'])
        WorkAssignment.objects.create(
            service_request=service, worker=worker,
            task_description=task, assigned_by=employee
        )
        service.status = 'IN_PROGRESS'
        service.save()
        Notification.objects.create(
            customer=service.customer,
            message=f"Work has been assigned for your service #{service.tracking_id}. {worker.name} is working on your vehicle."
        )
        messages.success(request, f"Work assigned to {worker.name}!")
        return redirect('assign_work', service_id=service_id)
    return render(request, 'service_app/assign_work.html', {
        'service': service, 'workers': workers, 'assignments': assignments
    })


@employee_required
def update_service_status(request, service_id):
    service = get_object_or_404(ServiceRequest, id=service_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        service.status = new_status
        if new_status == 'COMPLETED':
            service.completed_at = timezone.now()
            service.save()
            Notification.objects.create(
                customer=service.customer,
                message=f"🎉 Great news! Your vehicle service #{service.tracking_id} is COMPLETED. Please visit us for pickup."
            )
            messages.success(request, "Service marked completed. Customer notified!")
        else:
            service.save()
            messages.success(request, f"Status updated to {new_status}")
    return redirect('employee_dashboard')


@employee_required
def process_payment(request, service_id):
    service = get_object_or_404(ServiceRequest, id=service_id)
    existing_payment = Payment.objects.filter(service_request=service).first()
    if request.method == 'POST':
        method = request.POST.get('method')
        amount = Decimal(request.POST.get('amount', service.estimated_amount))
        txn_id = request.POST.get('transaction_id', '').strip()
        if existing_payment:
            payment = existing_payment
        else:
            payment = Payment(service_request=service)
        payment.amount = amount
        payment.method = method
        payment.transaction_id = txn_id
        payment.status = 'COMPLETED'
        payment.paid_at = timezone.now()
        payment.save()
        service.status = 'DELIVERED'
        service.save()
        Notification.objects.create(
            customer=service.customer,
            message=f"✅ Payment of ₹{amount} received for service #{service.tracking_id}. Receipt: {payment.receipt_number}. Thank you!"
        )
        messages.success(request, "Payment recorded successfully!")
        return redirect('generate_receipt', payment_id=payment.id)
    return render(request, 'service_app/payment.html', {
        'service': service, 'existing_payment': existing_payment
    })


@employee_required
def generate_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'service_app/receipt.html', {'payment': payment})
