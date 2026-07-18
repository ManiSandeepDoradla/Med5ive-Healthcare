from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Doctors(models.Model):
    name = models.CharField(max_length=50)
    specialization=models.CharField(max_length=50)
    description=models.TextField()
    photo_url=models.URLField()
    avail_location=models.CharField(max_length=50)
    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
    
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    full_name = models.CharField()
    email = models.CharField()
    phone_number = models.CharField()
    age = models.CharField(max_length=3)
    Appointment_type = models.CharField()
    cab_service = models.CharField()
    description = models.CharField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} with {self.doctor.name}"