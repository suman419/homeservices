from django.contrib import admin

# Register your models here.
from .models import Service, City, ServiceType, ServiceCharge, BookAppointment ,Contact, PhoneOTP, CallbackRequest, Career

admin.site.register(City)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(ServiceCharge)
admin.site.register(BookAppointment)
admin.site.register(Contact)
admin.site.register(PhoneOTP)
admin.site.register(CallbackRequest)
admin.site.register(Career)