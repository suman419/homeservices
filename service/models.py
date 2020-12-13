from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=25,db_index=True, unique=True)
    pincode = models.PositiveIntegerField()
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ('city_name',)
        
    def __str__(self):
        return self.city_name

class Service(models.Model):
    multiple_city = models.ManyToManyField(City)
    service_name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to="images", blank=True)
    slug = models.SlugField(max_length=200,db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.service_name


class ServiceType(models.Model): 
    service_name = models.ForeignKey(Service, related_name='service_type', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100) 
    image = models.ImageField(upload_to="images", blank=True)
    slug = models.SlugField(max_length=200,db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ('service_type',)
        
    def __str__(self):
        return self.service_type

class ServiceCharge(models.Model):
    service_charge_name = models.ForeignKey(ServiceType, on_delete=models.CASCADE)   
    issue_type = models.CharField(max_length=200,blank=True, null= True)
    price = models.CharField(max_length=100, blank=False)   
    image = models.ImageField(upload_to="images", blank=True)
    slug = models.SlugField(max_length=200,db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.issue_type

class BookAppointment(models.Model):
    client_name = models.CharField(max_length=100, blank=False)
    mobile = models.PositiveIntegerField(max_length =12, unique = True)
    email = models.EmailField()
    address = models.CharField(max_length=200, blank=False)
    landmark = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=50)
    appointment_date = models.CharField(max_length=200, blank=False, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.client_name

class Contact(models.Model):
    name=models.CharField(max_length=256)
    email=models.EmailField(blank=True)
    phone=models.IntegerField(blank=True)
    body=models.TextField(blank=True)
    service_type=models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone       = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp         = models.CharField(max_length=9, blank = True, null=True)
    count       = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated   = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp) 

class CallbackRequest(models.Model):
    name=models.CharField(max_length=256)
    mobile=models.IntegerField(blank=True)
    body=models.TextField(blank=True)
    callback_timing =models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Career(models.Model):
    name=models.CharField(max_length=256)
    mobile=models.IntegerField(blank=True)
    message=models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name