from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Doctors,Appointment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime, date, time
from django.contrib import messages
from django.contrib.messages import success,error
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.

def main(request):
    doctors=Doctors.objects.all().order_by('id')
    #return JsonResponse(doctors,safe=False)
    jdata=[]
    for data in doctors:
        tdata={
            'name':data.name,
            'specialization':data.specialization,
            'description':data.description,
            'photo_url':data.photo_url,
            'avail_location':data.avail_location
        }
        jdata.append(tdata)
    #return JsonResponse(jdata)
    return render(request,'main.html',{'doctors':jdata})

def profile_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id=request.POST['id']
            doctor=Doctors.objects.all()
            doctor=Doctors.objects.get(id=id)
            return render(request,'profile_page.html',{'doctor':doctor})
    return redirect('login')

def filter(request):
    if request.method=="POST":
        location=request.POST['location']
        specialization=request.POST['specialization']
        doctors=Doctors.objects.all()
        if specialization:
            doctors=doctors.filter(specialization=specialization)
        if location:
            doctors=doctors.filter(avail_location=location)
        return render(request,'main.html',{'doctors':doctors})
    return redirect('/')

def filter1(request):
    if request.method=="POST":
        doctors=Doctors.objects.all()
        doctors=doctors.exclude(specialization='psychiatrist')
        print(doctors)
        return render(request,'main.html',{'doctors':doctors})
    return redirect('/')

def filter2(request):
    if request.method=="POST":
        doctors=Doctors.objects.all()
        doctors=doctors.filter(specialization='psychiatrist')
        return render(request,'main.html',{'doctors':doctors})
    return redirect('/')

def my_appointments(request):
    if request.user.is_authenticated:
        qs = (
        Appointment.objects
        .filter(user_id=request.user.id)
        .select_related('doctor')
        .order_by('-date', '-time')
        )

        data = [
            {
                "id": a.id,
                "doctor": {
                    "name": a.doctor.name,
                    "specialization": a.doctor.specialization,
                    "photo_url": a.doctor.photo_url,
                    "avail_location": a.doctor.avail_location,
                },
                "full_name": a.full_name,
                "email": a.email,
                "phone_number": a.phone_number,
                "age": a.age,
                "appointment_type": a.Appointment_type,
                "cab_service": a.cab_service,
                "description": a.description,
                "date": a.date.isoformat(),
                "time": a.time.strftime("%H:%M:%S"),
                "created_at": a.created_at.isoformat(),
            }
            for a in qs
        ]
        today = timezone.localdate()
        
        completed_count = Appointment.objects.filter(date__lt=today,user_id=request.user.id).count()
        today_count     = Appointment.objects.filter(date=today,user_id=request.user.id).count()
        upcoming_count  = Appointment.objects.filter(date__gt=today,user_id=request.user.id).count()

        return render(request,'my_appointments.html',{'total':len(data),'appointments':data,'completed_count':completed_count,'upcoming_count':upcoming_count,'today_count':today_count})
    return redirect('login')

def book_appointment_step1(request):
    if request.method == 'POST':
        user_id = request.user.id
        doctor_id = request.POST['doctor_id']
        doctor_specialization = request.POST['doctor_specialization']
        full_name = request.POST['patientName']
        email = request.POST['patientEmail']
        phone_number = request.POST['patientPhone']
        age = request.POST['patientAge']
        appointment_type = request.POST['appointmentType']
        date_str = request.POST['appointmentDate'] 
        time_str = request.POST['selectedTime'] 
        description = request.POST['visitReason']
        
 
        
        cab_service_raw = request.POST['cabService']
 
        
        display_time=time_str
        input_value_time=time_str
        
        try:
           
            time_obj = datetime.strptime(time_str, "%H:%M")
            display_time = time_obj.strftime("%I:%M %p") 
            input_value_time = time_str 
        except ValueError:
            pass
        appointment_data = {
            'user_id': user_id,
            'doctor_id': doctor_id,
            'doctor_specialization':doctor_specialization,
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'age': age,
            'appointment_type': appointment_type,
            'cab_service': cab_service_raw,
            'date': date_str,
            'time': input_value_time,      
            'display_time': display_time,   
            'description': description,
        }
        print(appointment_data,"in bookings")
        booked_appontements = Appointment.objects.all()
        try:
            final_time = datetime.strptime(appointment_data['time'], "%I:%M %p").time()
        except ValueError:
            return HttpResponse("Invalid Date or Time format")
        if booked_appontements.filter(doctor_id=doctor_id,date=date_str,time=final_time).exists():
            messages.info(request,'slot is already booked please choose another slot')
            error(request,'the slot is already booked by some one please chose another')
            return render(request,'message_popup.html')
        else:
            show_popup=True
            request.session['temp_appt_data'] = appointment_data
            data = request.session.get('temp_appt_data')
            return render(request,'profile_page.html',{'show_popup':show_popup,'data':data})
    return redirect(to='/')
 
    

def confirm_appointment(request):
    data = request.session.get('temp_appt_data')
    if not data:
        return redirect('book_appointment_step1')
 
    
    user_obj = get_object_or_404(User, pk=data['user_id'])
    doctor_obj = get_object_or_404(Doctors, pk=data['doctor_id'])
 
    try:
        final_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        
        final_time = datetime.strptime(data['time'], "%I:%M %p").time()
    except ValueError:
        return HttpResponse("Invalid Date or Time format")
 
   
    Appointment.objects.create(
        user=user_obj,
        doctor=doctor_obj,
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        age=data['age'],
        Appointment_type=data['appointment_type'],
        cab_service=data['cab_service'],
        description=data['description'],
        date=final_date,
        time=final_time
    )
 
   
    del request.session['temp_appt_data']
    success(request,"yor oppointment is conformed!")
    return redirect(to='/')