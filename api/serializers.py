from rest_framework import serializers
from .models import Doctor, Patient, Assistant, Treatment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        # depth = 1
        fields = '__all__'

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        # depth = 1
        fields = '__all__'

class DoctorPatientTreatmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description', 'patient']

class PatientAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'assistants']

class TreatmentAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'assistant']
        
class DoctorPatientsReportSerializer(serializers.ModelSerializer):
    patients = PatientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'patients']        
