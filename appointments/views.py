from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Doctor
from .models import Patient
from .models import Appointment
from .models import Availability

def home_view(request):
    return render(request,'appointments/home.html')

def register_user(request):
    if request.method=='POST':

        # get data submitted from the form
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        address=request.POST.get('address')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('register')

        
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Patient.objects.create(
            user=user,
            phone=phone,
            age=age,
            gender=gender,
            address=address
        )

        messages.success(
            request,'Registration successful.'
        )
        return redirect('login')

    return render(request,'appointments/register.html')


def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'invalid username or passwords.'
            )

    return render(
        request,'appointments/login.html'
    )


def logout_user(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    upcoming_appointments = appointments.filter(
        status__in=['Pending', 'Approved']
    )

    approved_appointments = appointments.filter(
        status='Approved'
    ).count()

    pending_appointments = appointments.filter(
        status='Pending'
    ).count()

    completed_appointments = appointments.filter(
        status='Completed'
    ).count()

    return render(
        request,
        'appointments/dashboard.html',
        {
            'patient': patient,
            'appointments': appointments,
            'upcoming_appointments': upcoming_appointments,
            'approved_appointments': approved_appointments,
            'pending_appointments': pending_appointments,
            'completed_appointments': completed_appointments
        }
    )

def doctors(request):
    # display all doctors
    doctor_list=Doctor.objects.all()
    return render(request,'appointments/doctors.html',{'doctors':doctor_list})


def doctor_detail(request,doctor_id):
    # get doc
    doctor=get_object_or_404(Doctor,id=doctor_id)
    return render(request,'appointments/doctor_details.html',{'doctor':doctor})

def book_appointment(request,doctor_id):
    # user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    doctor=get_object_or_404(Doctor,id=doctor_id)
    patient=get_object_or_404(Patient,user=request.user)

    availabilities = Availability.objects.filter(
        doctor=doctor,
        is_available=True
    ).order_by('date','start_time')

    if request.method=='POST':
        appointment_date=request.POST.get(
            'appointment_date'
        )
        appointment_time=request.POST.get('appointment_time')

        reason=request.POST.get('reason')

        available = Availability.objects.filter(
            doctor=doctor,
            date=appointment_date,
            start_time__lte=appointment_time,
            end_time__gte=appointment_time,
            is_available=True
        ).exists()

        if not available:
            messages.error(
                request,
                'Doctor is not available at this date and time.'
            )
            return redirect(
                'book_appointment',
                doctor_id=doctor.id
            )

        existing_appointment=Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=['Pending','Approved']
        ).exists()

        if existing_appointment:
            messages.error(
                request,
                'This time slot is already booked'
            )
            return redirect('book_appointment',doctor_id=doctor.id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_time=appointment_time,
            appointment_date=appointment_date,
            reason=reason,
            status='Pending'
        )
        messages.success(
            request,
            'Appointment booked successfully.'
        )

        return redirect('my_appointments')
    return render(request,'appointments/book_appointment.html',
                  {'doctor':doctor,'availabilities': availabilities})

def my_appointments(request):
    if not request.user.is_authenticated:
        return redirect('login')

    patient=get_object_or_404(
        Patient,
        user=request.user
    )

    appointments=Appointment.objects.filter(
        patient=patient
    ).order_by('-appointment_date')
    return render(request,'appointments/my_appointment.html',{'appointments':appointments})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    patient=get_object_or_404(
        Patient,
        user=request.user
    )
    return render(
        request,
        'appointments/profile.html',{'patient':patient}
    )

def doctor_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            if hasattr(user,'doctor'):
                login(request,user)
                return redirect('doctor_dashboard')
            else:
                messages.error(
                    request,
                    'This account is not registered as a doctor.'
                )
        else:
            messages.error(
                    request,
                    'Invalid username or password,'
            )
    return render(request,'appointments/doctor_login.html')


def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    return render(
        request,
        'appointments/doctor_dashboard.html',
        {
            'doctor': doctor,
            'appointments': appointments
        }
    )

def approve_appointment(request,appointment_id):
    if not request.user.is_authenticated:
        return redirect('doctor_login')
    doctor=get_object_or_404(Doctor,user=request.user)

    appointment=get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    appointment.status='Approved'
    appointment.save()

    messages.success(request,'Appointment approved successfully.')
    return redirect('doctor_dashboard')

def reject_appointment(request,appointment_id):
    if not request.user.is_authenticated:
        return redirect('doctor_login')
    doctor=get_object_or_404(Doctor,user=request.user)
    appointment=get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    appointment.status='Rejected'
    appointment.save()

    messages.success(request,'Appointment rejected.')
    return redirect('doctor_dashboard')

def complete_appointment(request, appointment_id):
    if not request.user.is_authenticated:
        return redirect('doctor_login')
    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )
    appointment.status = 'Completed'
    appointment.save()
    messages.success(
        request,
        'Appointment marked as completed.'
    )
    return redirect('doctor_dashboard')

def doctor_availability(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        Availability.objects.create(
            doctor=doctor,
            date=date,
            start_time=start_time,
            end_time=end_time,
            is_available=True
        )

        messages.success(
            request,
            'Availability added successfully.'
        )

        return redirect('doctor_availability')

    availabilities = Availability.objects.filter(
        doctor=doctor
    ).order_by(
        'date',
        'start_time'
    )

    return render(
        request,
        'appointments/doctor_availability.html',
        {
            'doctor': doctor,
            'availabilities': availabilities
        }
    )


def edit_availability(request, availability_id):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    availability = get_object_or_404(
        Availability,
        id=availability_id,
        doctor=doctor
    )

    if request.method == 'POST':
        availability.date = request.POST.get('date')
        availability.start_time = request.POST.get('start_time')
        availability.end_time = request.POST.get('end_time')
        availability.is_available = request.POST.get('is_available') == 'on'

        availability.save()

        messages.success(
            request,
            'Availability updated successfully.'
        )

        return redirect('doctor_availability')

    return render(
        request,
        'appointments/edit_availability.html',
        {
            'availability': availability
        }
    )


def delete_availability(request, availability_id):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    availability = get_object_or_404(
        Availability,
        id=availability_id,
        doctor=doctor
    )

    availability.delete()

    messages.success(
        request,
        'Availability deleted successfully.'
    )

    return redirect('doctor_availability')