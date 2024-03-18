from django.contrib import admin
from .models import Doctor, Patient, Assistant, Treatment

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Assistant)
admin.site.register(Treatment)