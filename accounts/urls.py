from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('employee-login/', views.employee_login, name='employee_login'),
    path('register/', views.customer_register, name='customer_register'),
    path('verify-register/', views.verify_register, name='verify_register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.my_profile, name='my_profile'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/export/', views.export_bookings_excel, name='export_bookings_excel'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]
