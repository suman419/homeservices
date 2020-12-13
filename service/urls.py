from django.contrib import admin
from django.urls import path
from service import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('contact', views.contact, name = 'contact'),
    path('about', views.about, name = 'about'),
    path('career', views.career, name = 'career'),
    path('service_detail', views.service_detail,name='service_detail'),
    path('service_list', views.list_service,name='service_list'),
    path('service/<str:name>', views.service,name='service'),
    path('service/<str:service_name>/booking_confirm', views.mobile_otp_send, name="booking_confirm"),
    path('service/<str:service_name>/booking_completed', views.validate, name="booking_completed"),
    path('service/<str:service_name>/booking_completed/success', views.success, name="success"),
    path('create_career', views.create_career, name = 'create_career'),
    path('create_contact', views.create_contact_us, name = 'create_contact'),
    path('service/<str:service_name>/create_callback_request', views.create_callback_request, name = 'create_callback_request'),
]

app_name = 'service'
