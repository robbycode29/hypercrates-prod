from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import DoctorViewSet, PatientViewSet, AssistantViewSet, TreatmentViewSet, DoctorPatientTreatmentsView, PatientAssistantView, TreatmentAssistantView, PatientTreatmentsReportView, DoctorsPatientsReportView

router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctors')
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'assistants', AssistantViewSet, basename='assistants')
router.register(r'treatments', TreatmentViewSet, basename='treatments')
router.register(r'doctors/(?P<doctor_id>[^/.]+)/patients/(?P<patient_id>[^/.]+)/treatments', DoctorPatientTreatmentsView, basename='doctor_patient_treatments')
router.register(r'patients/(?P<patient_id>[^/.]+)/treatments/report', PatientTreatmentsReportView, basename='patient_treatments_report')
router.register(r'report', DoctorsPatientsReportView, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('patients/<int:pk>/assistants/', PatientAssistantView.as_view({'put': 'update', 'get': 'retrieve'}), name='patient_assistants'),
    path('treatments/<int:pk>/assistant/', TreatmentAssistantView.as_view({'put': 'update', 'get': 'retrieve'}), name='treatment_assistant'),
]