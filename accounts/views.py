from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import json
from django.utils import timezone
from django.db.models import Count
from bookings.models import Booking
import csv
from django.http import HttpResponse
from bookings.models import Booking # Adjust import based on your structure

from .models import User, Employee, OTPVerification, Notification


def send_otp(mobile_number, otp, purpose='login'):
    """
    Send OTP via SMS. Integrate with Fast2SMS, Twilio, or MSG91.
    For development, OTP is printed to console.
    """
    print(f"[DEV] OTP for {mobile_number} ({purpose}): {otp}")
    # Production: Use Fast2SMS API
    # import requests
    # url = "https://www.fast2sms.com/dev/bulkV2"
    # payload = {"route":"v3","sender_id":"SMTRPR","message":f"Your Smart Repair OTP is {otp}. Valid for 10 minutes.","language":"english","flash":0,"numbers":mobile_number}
    # headers = {"authorization": settings.SMS_API_KEY, "Content-Type": "application/json"}
    # requests.post(url, json=payload, headers=headers)
    return True


@ensure_csrf_cookie
def customer_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    step = request.session.get('login_step', 'mobile')
    mobile = request.session.get('login_mobile', '')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send_otp':
            mobile_number = request.POST.get('mobile_number', '').strip()
            if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
                messages.error(request, 'Please enter a valid 10-digit mobile number.')
                return render(request, 'accounts/customer_login.html', {'step': 'mobile'})

            otp_obj = OTPVerification.generate_otp(mobile_number, purpose='login')
            send_otp(mobile_number, otp_obj.otp, 'login')
            request.session['login_step'] = 'otp'
            request.session['login_mobile'] = mobile_number
            messages.info(request, f'OTP sent to {mobile_number[-4:].zfill(10)[:6]}****{mobile_number[-4:]}')
            return render(request, 'accounts/customer_login.html', {'step': 'otp', 'mobile': mobile_number})

        elif action == 'verify_otp':
            mobile_number = request.session.get('login_mobile')
            otp_entered = request.POST.get('otp', '').strip()

            otp_obj = OTPVerification.objects.filter(
                mobile_number=mobile_number,
                otp=otp_entered,
                purpose='login',
                is_used=False
            ).first()

            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()

                user, created = User.objects.get_or_create(
                    mobile_number=mobile_number,
                    defaults={'role': 'customer', 'is_verified': True}
                )

                if created:
                    user.set_unusable_password()
                    user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session.pop('login_step', None)
                request.session.pop('login_mobile', None)

                if created or not user.first_name:
                    messages.success(request, 'Welcome! Please complete your profile.')
                    return redirect('complete_profile')
                else:
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
                return render(request, 'accounts/customer_login.html', {'step': 'otp', 'mobile': mobile_number})

    return render(request, 'accounts/customer_login.html', {'step': step, 'mobile': mobile})


@ensure_csrf_cookie
def employee_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()

        if not employee_id or not mobile_number:
            messages.error(request, 'Please enter both Employee ID and Mobile Number.')
            return render(request, 'accounts/employee_login.html')

        try:
            employee = Employee.objects.get(employee_id=employee_id, user__mobile_number=mobile_number, is_active=True)
            user = employee.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, f'Welcome, {user.get_full_name()}! Employee Dashboard')
            return redirect('employee_dashboard')
        except Employee.DoesNotExist:
            messages.error(request, 'Invalid Employee ID or Mobile Number. Please check your credentials.')

    return render(request, 'accounts/employee_login.html')

def export_bookings_excel(request):
    # Get filters from request if any
    status = request.GET.get('status')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Booking ID', 'Customer', 'Vehicle', 'Status', 'Date'])
    
    bookings = Booking.objects.all()
    if status:
        bookings = bookings.filter(status=status)
        
    for b in bookings:
        writer.writerow([b.booking_id, b.customer.get_full_name() or b.customer.mobile_number, b.vehicle.vehicle_number, b.booking_date.strftime('%d %b %Y'), b.get_booking_type_display().upper(), b.get_status_display().upper(), b.estimated_total])
        
    return response




@ensure_csrf_cookie
def customer_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        mobile = request.POST.get('mobile_number', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()

        if User.objects.filter(mobile_number=mobile).exists():
            messages.error(request, 'A user with this mobile number already exists. Please login.')
            return redirect('customer_login')

        otp_obj = OTPVerification.generate_otp(mobile, purpose='register')
        send_otp(mobile, otp_obj.otp, 'register')

        request.session['reg_data'] = {
            'mobile': mobile,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'address': address,
            'city': city,
        }
        messages.info(request, f'OTP sent to your mobile number ending in {mobile[-4:]}')
        return render(request, 'accounts/verify_register.html', {'mobile': mobile})

    return render(request, 'accounts/register.html')


def verify_register(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        reg_data = request.session.get('reg_data', {})
        mobile = reg_data.get('mobile')

        if not mobile:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('customer_register')

        otp_obj = OTPVerification.objects.filter(
            mobile_number=mobile, otp=otp_entered, purpose='register', is_used=False
        ).first()

        if otp_obj and otp_obj.is_valid():
            otp_obj.is_used = True
            otp_obj.save()

            user = User.objects.create(
                mobile_number=mobile,
                first_name=reg_data.get('first_name', ''),
                last_name=reg_data.get('last_name', ''),
                email=reg_data.get('email', ''),
                address=reg_data.get('address', ''),
                city=reg_data.get('city', ''),
                role='customer',
                is_verified=True,
            )
            user.set_unusable_password()
            user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            request.session.pop('reg_data', None)
            messages.success(request, f'Registration successful! Welcome, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')

    return render(request, 'accounts/verify_register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def complete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.address = request.POST.get('address', '').strip()
        user.city = request.POST.get('city', '').strip()
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')
    return render(request, 'accounts/complete_profile.html')


@login_required
def my_profile(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    return render(request, 'accounts/profile.html', {'notifications': notifications})


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': notifs})


@login_required
def employee_dashboard(request):
    if request.user.role not in ['employee', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    try:
        employee = request.user.employee_profile
        center = employee.service_center
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)

        # 1. Fetch exactly what you need for the table (Recent 20)
        recent_bookings = Booking.objects.filter(service_center=center).order_by('-created_at')[:20]

        # 2. Global counts for the center (Not limited to the top 20)
        pending = Booking.objects.filter(service_center=center, status='pending').count()
        in_progress = Booking.objects.filter(service_center=center, status='in_progress').count()
        
        # 3. Completed Today
        completed_today = Booking.objects.filter(
            service_center=center, 
            status='completed', 
            completed_at__date=today
        ).count()

        # 4. Total This Month (All statuses)
        total_this_month = Booking.objects.filter(
            service_center=center,
            created_at__date__gte=first_day_of_month
        ).count()

    except Exception as e:
        # It's better to log the error than a bare except
        print(f"Dashboard Error: {e}")
        employee = None
        recent_bookings = []
        pending = in_progress = completed_today = total_this_month = 0

    return render(request, 'accounts/employee_dashboard.html', {
        'employee': employee,
        'bookings': recent_bookings,
        'pending': pending,
        'in_progress': in_progress,
        'completed_today': completed_today,
        'total_this_month': total_this_month,
    })

def resend_otp(request):
    if request.method == 'POST':
        mobile = request.session.get('login_mobile') or request.POST.get('mobile')
        purpose = request.POST.get('purpose', 'login')
        if mobile:
            otp_obj = OTPVerification.generate_otp(mobile, purpose=purpose)
            send_otp(mobile, otp_obj.otp, purpose)
            return JsonResponse({'success': True, 'message': 'OTP resent successfully!'})
    return JsonResponse({'success': False, 'message': 'Failed to resend OTP.'})
