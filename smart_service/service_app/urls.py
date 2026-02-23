from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('track/', views.track_service, name='track_service'),

    # Customer auth
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/send-otp/', views.send_customer_otp, name='send_customer_otp'),
    path('customer/verify-otp/', views.verify_customer_otp, name='verify_customer_otp'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),

    # Employee auth
    path('employee/login/', views.employee_login, name='employee_login'),
    path('employee/logout/', views.employee_logout, name='employee_logout'),

    # Employee dashboard
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/add-service/', views.add_service_request, name='add_service_request'),
    path('employee/verify-vehicle-otp/', views.verify_vehicle_otp, name='verify_vehicle_otp'),
    path('employee/send-vehicle-otp/', views.send_vehicle_otp, name='send_vehicle_otp'),
    path('employee/assign-work/<int:service_id>/', views.assign_work, name='assign_work'),
    path('employee/update-status/<int:service_id>/', views.update_service_status, name='update_service_status'),
    path('employee/payment/<int:service_id>/', views.process_payment, name='process_payment'),
    path('employee/receipt/<int:payment_id>/', views.generate_receipt, name='generate_receipt'),

    # Service tracking
    path('service/track/<str:tracking_id>/', views.service_detail, name='service_detail'),
]
