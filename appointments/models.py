from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# stores doctors info

class Doctor(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    specialization=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    experience=models.PositiveIntegerField()
    description=models.TextField(blank=True)

    def __str__(self):
        # name will appear in django admin
        return self.name


class Patient(models.Model):
    # connect patient with django built in user
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=20)
    address=models.TextField()

    def __str__(self):
        return self.user.username


class Availability(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)

    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.name}-{self.date}"


class Appointment(models.Model):
    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    ]
    # patient who booked appointment
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    # doctor selected by patient
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)

    appointment_date=models.DateField()

    appointment_time=models.TimeField()

    reason=models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # automatically stores booking time
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient}-{self.doctor}-{self.appointment_date}"

    
