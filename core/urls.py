from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services_list, name='services_list'),
    path('service-centers/', views.service_centers_list, name='service_centers'),
    path('service-centers/<int:pk>/', views.service_center_detail, name='center_detail'),
    path('track-service/', views.track_service, name='track_service'),
    path('holidays/', views.holidays, name='holidays'),
    path('api/centers/', views.get_centers_api, name='centers_api'),
]
