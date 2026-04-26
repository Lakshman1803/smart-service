from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import ServiceCenter, Holiday, ServiceType, ContactMessage


def home(request):
    service_centers = ServiceCenter.objects.filter(is_active=True)[:6]
    services = ServiceType.objects.filter(is_active=True)[:8]
    upcoming_holidays = Holiday.objects.filter(date__gte=timezone.now().date()).order_by('date')[:5]
    all_holidays = Holiday.objects.filter(date__year=timezone.now().year).order_by('date')

    context = {
        'service_centers': service_centers,
        'services': services,
        'upcoming_holidays': upcoming_holidays,
        'all_holidays': all_holidays,
        'total_centers': ServiceCenter.objects.filter(is_active=True).count(),
        'total_services': ServiceType.objects.filter(is_active=True).count(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name, mobile=mobile, email=email,
            subject=subject, message=message
        )
        messages.success(request, 'Your message has been sent! We will contact you shortly.')
        return redirect('contact')

    return render(request, 'core/contact.html')


def service_centers_list(request):
    centers = ServiceCenter.objects.filter(is_active=True).order_by('city')
    cities = centers.values_list('city', flat=True).distinct()
    city_filter = request.GET.get('city', '')
    if city_filter:
        centers = centers.filter(city__icontains=city_filter)
    return render(request, 'core/service_centers.html', {
        'centers': centers, 'cities': cities, 'city_filter': city_filter
    })


def service_center_detail(request, pk):
    center = get_object_or_404(ServiceCenter, pk=pk, is_active=True)
    return render(request, 'core/center_detail.html', {'center': center})


def services_list(request):
    vehicle_type = request.GET.get('type', 'all')
    services = ServiceType.objects.filter(is_active=True)
    if vehicle_type != 'all':
        services = services.filter(vehicle_type__in=[vehicle_type, 'all'])
    return render(request, 'core/services_list.html', {
        'services': services, 'vehicle_type': vehicle_type
    })


def track_service(request):
    booking = None
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        mobile = request.POST.get('mobile')
        from bookings.models import Booking
        try:
            booking = Booking.objects.get(
                booking_id=booking_id,
                customer__mobile_number=mobile
            )
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found. Please check your Booking ID and Mobile Number.')

    return render(request, 'core/track_service.html', {'booking': booking})


def holidays(request):
    current_year = timezone.now().year
    all_holidays = Holiday.objects.filter(date__year=current_year).order_by('date')
    return render(request, 'core/holidays.html', {'holidays': all_holidays, 'year': current_year})


def get_centers_api(request):
    centers = ServiceCenter.objects.filter(is_active=True).values(
        'id', 'name', 'city', 'address', 'phone', 'latitude', 'longitude',
        'working_hours', 'working_days'
    )
    return JsonResponse({'centers': list(centers)})


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)
