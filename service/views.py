from django.shortcuts import render, redirect
from service.models import Service, City, ServiceType, ServiceCharge, BookAppointment, PhoneOTP, Career, Contact, CallbackRequest
from math import ceil
from django.forms.models import model_to_dict

from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import http.client

import json
import requests
import ast
import random

conn = http.client.HTTPConnection("2factor.in")
api_key = "aac35574-3852-11eb-83d4-0200cd936042"
template_name = "A2Zhomeservice"

 
# Create your views here.
def index(request):
    all_city = City.objects.all()
    all_services= Service.objects.all()
    n = len(all_services)
    nSlides= n//4 + ceil((n/4) - (n//4))
    allservices=[[all_services, range(1, len(all_services)), nSlides],[all_services, range(1, len(all_services)), nSlides]]
    params={'cities':all_city,'range': range(nSlides), 'no_of_slides':nSlides,'allservices':allservices, 'services':all_services}
    return render(request,"index.html", params)
   

def list_service(request):
    list_services= Service.objects.all()
    n = len(list_services)
    query = request.GET.get("search")
    if query:
        list_services = list_services.filter(
            Q(service_name__icontains=query) |
            Q(city__icontains=query))
    nSlides= n//4 + ceil((n/4) - (n//4))
    params={'range': range(nSlides), 'no_of_slides':nSlides,'services':list_services, }
    return render(request,'list_service.html', params)   

def service_detail(request):
    if request.method =="POST":
        city_id =request.POST['city']
        service_name =request.POST['service']
        # service = Service.objects.get(multiple_city=city_id,service_name=service_name)
        # return render(request, 'service_detail.html',  {'service':service})   
        service_detail = Service.objects.get(service_name = service_name)
        service_type = ServiceType.objects.filter(service_name = service_detail.id)
        ser_type = []
        for stype in service_type:
            ser_type.append(stype.service_type)  
        serv_list = []
        dic_obj = {}
        for charge in service_type:
            service_name = charge.service_type
            service_charge= ServiceCharge.objects.filter(service_charge_name_id=charge.id)
            dic_obj[service_name] = service_charge
            serv_list.append(dic_obj)
        service_charge=[]
        for i in range(len(serv_list)):
            if serv_list[i] not in serv_list[i+1:]:
                service_charge.append(serv_list[i])
        return render(request, 'service.html',  {'service_detail':service_detail,'service_type':service_type,'service_charge':service_charge,'ser_type':ser_type})    


def service(request, name):
    service_detail = Service.objects.get(service_name = name)
    service_type = ServiceType.objects.filter(service_name = service_detail.id)
    ser_type = []
    for stype in service_type:
        ser_type.append(stype.service_type)  
    serv_list = []
    dic_obj = {}
    for charge in service_type:
        service_name = charge.service_type
        service_charge= ServiceCharge.objects.filter(service_charge_name_id=charge.id)
        dic_obj[service_name] = service_charge
        serv_list.append(dic_obj)
    service_charge=[]
    for i in range(len(serv_list)):
        if serv_list[i] not in serv_list[i+1:]:
            service_charge.append(serv_list[i])
    return render(request, 'service.html',  {'service_detail':service_detail,'service_type':service_type,'service_charge':service_charge,'ser_type':ser_type})    
    
    
def booking_confirm(request):
    return render(request,'confirm_booking.html', )  

def contact(request):
    return render(request,'contact.html', )

def about(request):
    return render(request,'about.html', )  

def career(request):
    return render(request,'career.html', )       

def success(request):
    return render(request,'success.html', )      


def mobile_otp_send(request, service_name):
    if request.method == 'POST':
        phone_number =request.POST.get('mobile')
        appointment_date = request.POST.get('date')
        requirement = request.POST.get('requirement')
        
        if phone_number:
            phone = str(phone_number)
            otp = send_otp(phone)
            if otp:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    count = old.count
                    if count > 5:
                        messages.error(request,  "Sending otp error. Limit Exceeded. Please Contact Customer support.")
                        return redirect('index.html')
                        
                    old.count = count +1
                    old.save()
                    url=f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/{template_name}"
                    conn.request("GET", url)
                    res = conn.getresponse()            
                    data = res.read()
                    data=data.decode("utf-8")
                    data=ast.literal_eval(data)
                    if data["Status"] == 'Success':
                        old.otp_session_id = data["Details"]
                        old.save()
                        print('In validate phone :'+old.otp_session_id)
                        messages.success(request,  "OTP sent successfully on your mobile.")
                        return render(request, 'confirm_booking.html',{'requirement':requirement,'phone_number':phone_number,'appointment_date':appointment_date})            
                    else:
                        messages.error(request, "Sending otp Failed.")
                        return HttpResponseRedirect('/')           
                else:
                    obj=PhoneOTP.objects.create(
                            phone=phone_number,
                            otp = otp,
                            )
                    url=f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/{template_name}"
                    conn.request("GET", url)
                    res = conn.getresponse()            
                    data = res.read()
                    data=data.decode("utf-8")
                    data=ast.literal_eval(data)

                    if data["Status"] == 'Success':
                        obj.otp_session_id = data["Details"]
                        obj.save()
                        print('In validate phone :'+obj.otp_session_id)
                        messages.success(request, "OTP sent successfully on your mobile.")
                        return render(request, 'confirm_booking.html', {'requirement':requirement,'phone_number':phone_number,'appointment_date':appointment_date} )  
                          
                    else:
                        messages.error(request, "Sending otp Failed.")
                        return redirect('') 
            else:
                messages.error(request,  "Sending otp error.")
                return redirect('') 
        else:
            messages.error(request,  "Phone number is not provided.")
            return HttpResponseRedirect('/')                  
    return HttpResponseRedirect('/')           

          
def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False          

def validate(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        landmark = request.POST.get('landmark', False)
        city = request.POST.get('city', False)
        appointment_date = request.POST.get('appointment_date', False)
        print(appointment_date)
        otp_sent = request.POST.get('otp', False)
        phone = request.POST.get('phone_number', False)
        description = request.POST.get('notes', False)
        print(description)
        if otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                validate_otp_url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{otp_session_id}/{otp_sent}"
                
                conn.request("GET", validate_otp_url)
                res = conn.getresponse()    
                data = res.read()
                print(data.decode("utf-8"))
                data=data.decode("utf-8")
                data=ast.literal_eval(data)
                if data["Status"] == 'Success':
                    old.validated = True
                    old.save()
                    booking_obj=BookAppointment.objects.create(
                            client_name=name,
                            mobile = phone,
                            email = email,
                            address = address,
                            landmark = landmark,
                            appointment_date = appointment_date,
                            description = description
                            )
                    messages.success(request, "OTP MATCHED. Your booking order is confirmed.")
                    return render(request, 'success.html')

                else:
                    messages.error(request, "OTP Not MATCHED. Enter valid otp.")
                    return redirect('booking_confirm')
                    
            else:
                messages.error(request, "First Proceed via sending otp request.")
                return redirect('booking_confirm')
                          
        else:
            messages.error(request, "Please provide otp for Validation.")
            return redirect('booking_confirm')
    return render(request, 'confirm_booking.html') 


def create_contact_us(request):
    if request.method == 'POST':
        phone_number =request.POST.get('mobile')
        name = request.POST.get('name')
        email =request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        try:
            contact_obj = Contact.objects.create(
                phone=phone_number,
                name = name,
                body = message,
                email=email,
                service_type=subject
            )
            messages.success(request,  "Message sent successfully.")
            return HttpResponseRedirect('/')
        except:
            messages.error(request,  "Failed to send message.")
            return render(request, 'contact.html')    
         

def create_career(request):
    if request.method == 'POST':
        phone_number =request.POST.get('mobile')
        name = request.POST.get('name')
        message = request.POST.get('message')
        try: 
            career_obj = Career.objects.create(
                mobile=phone_number,
                name = name,
                message = message
            )
            messages.success(request,  "Message sent successfully.")
            return HttpResponseRedirect('/') 
        except:
            messages.error(request,  "Failed to send message.")
            return render(request, 'career.html')       


def create_callback_request(request, *args, **kwargs):
    if request.method == 'POST':
        phone_number =request.POST.get('phone')
        print(phone_number)
        name = request.POST.get('name')
        print(name)
        callback_timing =request.POST.get('day')
        print(callback_timing)
        message = request.POST.get('message')
        print(message)
        try:
            contact_obj = CallbackRequest.objects.create(
                name = name,
                body = message,
                mobile=phone_number,
                callback_timing=callback_timing
            )
            messages.success(request,  "Message sent successfully.")
            return HttpResponseRedirect('/')
        except:
            messages.error(request,  "Failed to send message.")
            return render(request, 'contact.html')    