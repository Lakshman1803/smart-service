from django.urls import path
from . import views

urlpatterns = [
    path('bill/<int:pk>/', views.create_bill, name='create_bill'),
    path('bill/<int:pk>/finalize/', views.finalize_payment, name='finalize_payment'),
    path('online/<int:pk>/', views.online_payment, name='online_payment'),
    path('online/<int:pk>/confirm/', views.confirm_online_payment, name='confirm_online_payment'),
    path('receipt/<int:pk>/', views.view_receipt, name='view_receipt'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('upload-qr/', views.upload_qr_code, name='upload_qr_code'),
]
