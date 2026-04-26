from django.urls import path
from . import views

urlpatterns = [
    path('book/step1/', views.book_slot_step1, name='book_step1'),
    path('book/step2/', views.book_slot_step2, name='book_step2'),
    path('book/step3/', views.book_slot_step3, name='book_step3'),
    path('book/confirm/', views.confirm_booking, name='confirm_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    # Employee
    path('employee/bookings/', views.employee_bookings, name='employee_bookings'),
    path('employee/booking/<int:pk>/', views.employee_booking_detail, name='employee_booking_detail'),
    path('employee/booking/<int:pk>/verify-otp/', views.verify_customer_otp, name='verify_customer_otp'),
    path('employee/booking/<int:pk>/assign-workers/', views.assign_workers, name='assign_workers'),
    path('employee/booking/<int:pk>/complete/', views.complete_service, name='complete_service'),
    path('employee/booking/<int:pk>/add-charge/', views.add_extra_charge, name='add_extra_charge'),
    path('employee/charge/<int:charge_pk>/remove/', views.remove_charge, name='remove_charge'),
    path('employee/charge/<int:charge_pk>/update-price/', views.update_charge_price, name='update_charge_price'),
    path('employee/add-vehicle/', views.add_customer_vehicle, name='add_customer_vehicle'),
    path('api/slots/', views.get_available_slots, name='available_slots_api'),
]
