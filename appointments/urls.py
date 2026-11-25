from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    # display all doctors
    path('doctors/',views.doctors,name='doctors'),
    # display individual doctor
    path('doctor/<int:doctor_id>/',views.doctor_detail,name='doctor_detail'),
    # book appoinment
    path('book/<int:doctor_id>/',views.book_appointment,name='book_appointment'),
    # display patient's appoinments
    path('my-appointments/',views.my_appointments,name='my_appointments'),
    # profile
    path('profile/',views.profile,name='profile'),
    path('doctor-login/',views.doctor_login,name='doctor_login'),
    path('doctor-dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('appointment/<int:appoint_id>/approve/',views.approve_appointment,name='approve_appointment'),
    path('appointment/<int:appointment_id>/reject/',views.reject_appointment,name='reject_appointment'),
    path('appointment/<int:appointment_id>/complete/',views.complete_appointment,name='complete_appointment'),
    path('doctor-availability/',views.doctor_availability,name='doctor_availability'),
    path('doctor-availability/', views.doctor_availability, name='doctor_availability'),
path('doctor-availability/<int:availability_id>/edit/', views.edit_availability, name='edit_availability'),
path('doctor-availability/<int:availability_id>/delete/', views.delete_availability, name='delete_availability'),
]
