from rest_framework import status
from rest_framework.response import Response
import json
from django.db.models import Count, Avg
from .serializers import DoctorSerializer, PatientSerializer, AssistantSerializer, TreatmentSerializer, DoctorPatientTreatmentsSerializer, PatientAssistantSerializer, TreatmentAssistantSerializer, DoctorPatientsReportSerializer
from .models import Doctor, Patient, Assistant, Treatment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor, IsGeneralManager, IsAssistant
    
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsGeneralManager]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAuthenticated, IsGeneralManager]

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class DoctorPatientTreatmentsView(viewsets.ModelViewSet):
    serializer_class = DoctorPatientTreatmentsSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        patient_id = self.kwargs['patient_id']
        return Treatment.objects.filter(patient__id=patient_id, patient__doctor__id=doctor_id)

class PatientAssistantView(viewsets.ModelViewSet):
    serializer_class = PatientAssistantSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    lookup_field = 'pk'
    
    def get_queryset(self):
        patient_id = self.kwargs['pk']
        return Patient.objects.filter(id=patient_id)
    
    def create(self, request, *args, **kwargs):
        return Response({"detail": "Creation not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deletion not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        patient = self.get_object()
        assistant_ids = request.data.get('assistants')
        if isinstance(assistant_ids, str):
            assistant_ids = json.loads(assistant_ids)
        if not isinstance(assistant_ids, list):
            assistant_ids = [assistant_ids]
        if assistant_ids is not None:
            try:
                assistants = Assistant.objects.filter(id__in=assistant_ids)
                patient.assistants.set(assistants)
                patient.save()
                return Response(self.get_serializer(patient).data)
            except Assistant.DoesNotExist:
                return Response({'error': 'Assistant does not exist'}, status=400)
        else:
            return Response({'error': 'No assistant provided'}, status=400)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class TreatmentAssistantView(viewsets.ModelViewSet):
    serializer_class = TreatmentAssistantSerializer
    permission_classes = [IsAuthenticated, IsAssistant]
    lookup_field = 'pk'

    def get_queryset(self):
        treatment_id = self.kwargs['pk']
        return Treatment.objects.filter(id=treatment_id)
    
    def create(self, request, *args, **kwargs):
        return Response({"detail": "Creation not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deletion not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        treatment = self.get_object()
        assistant_id = request.data.get('assistant')
        if assistant_id is not None:
            try:
                assistant = Assistant.objects.get(id=assistant_id)
                treatment.assistant = assistant
                treatment.save()
                return Response(self.get_serializer(treatment).data)
            except Assistant.DoesNotExist:
                return Response({'error': 'Assistant does not exist'}, status=400)
        else:
            return Response({'error': 'No assistant provided'}, status=400)
        
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class PatientTreatmentsReportView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Treatment.objects.filter(patient__id=patient_id)
    
class DoctorsPatientsReportView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorPatientsReportSerializer
    permission_classes = [IsAuthenticated, IsGeneralManager]

    def get_queryset(self):
        return Doctor.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_patients = Patient.objects.count()
        avg_patients_per_doctor = Doctor.objects.annotate(num_patients=Count('patients')).aggregate(avg=Avg('num_patients'))['avg']
        data = {
            'statistics': {
                'total_patients': total_patients,
                'avg_patients_per_doctor': avg_patients_per_doctor,
            },
            'doctors': response.data
        }
        return Response(data)
