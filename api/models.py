from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    doctor = models.ForeignKey(Doctor, related_name='patients', on_delete=models.CASCADE)
    assistants = models.ManyToManyField('Assistant', related_name='patients', blank=True)

    def __str__(self):
        return self.name

class Assistant(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, related_name='treatments', on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, related_name='treatments', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"Treatment {self.name} for {self.patient.name}"