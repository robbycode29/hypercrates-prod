from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group

## Testing login
class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
    
    def test_login(self):
        url = reverse('api_token_auth')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

## Testing DoctorViewSet with GM permissions
class DoctorsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('doctors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update(self):
        url = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        doctor_id = response.data['id']
        url = reverse('doctors-detail', kwargs={'pk': doctor_id})
        data = {'name': 'Dr. John', 'specialization': 'Cardiology', 'user': self.user.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        doctor_id = response.data['id']
        url = reverse('doctors-detail', kwargs={'pk': doctor_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
## Testing DoctorViewSet with Doctor permissions
class DoctorsTestDoctor(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('doctors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        url = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
## Testing DoctorViewSet with Assistant permissions
class DoctorsTestAssistant(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='Assistant')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('doctors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        url = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
## Testing PatientViewSet
class PatientsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Switch to doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('patients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update(self):
        url = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response = self.client.post(url, data)
        patient_id = response.data['id']
        url = reverse('patients-detail', kwargs={'pk': patient_id})
        data = {'name': 'John Doe', 'age': 31, 'doctor': self.doctor_id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response = self.client.post(url, data)
        patient_id = response.data['id']
        url = reverse('patients-detail', kwargs={'pk': patient_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
## Testing AssistantViewSet
class AssistantsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('assistants-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('assistants-list')
        data = {'name': 'John Doe', 'user': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update(self):
        url = reverse('assistants-list')
        data = {'name': 'John Doe', 'user': self.user.id}
        response = self.client.post(url, data)
        assistant_id = response.data['id']
        url = reverse('assistants-detail', kwargs={'pk': assistant_id})
        data = {'name': 'John Doe (Modified)', 'user': self.user.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('assistants-list')
        data = {'name': 'John Doe', 'user': self.user.id}
        response = self.client.post(url, data)
        assistant_id = response.data['id']
        url = reverse('assistants-detail', kwargs={'pk': assistant_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
## Testing TreatmentViewSet
class TreatmentsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
        
        ## Switch to doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('treatments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update(self):
        url = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        treatment_id = response.data['id']
        url = reverse('treatments-detail', kwargs={'pk': treatment_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment (Modified)'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        treatment_id = response.data['id']
        url = reverse('treatments-detail', kwargs={'pk': treatment_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

## Testing DoctorPatientTreatmentsView
class DoctorPatientTreatmentsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
        
        ## Create a treatment
        url_treatments = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response_treatments = self.client.post(url_treatments, data)
        self.treatment_id = response_treatments.data['id']
        
        ## Switch to Doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)        
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    
    def test_list(self):
        url = reverse('doctor_patient_treatments-list', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('doctor_patient_treatments-list', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update(self):
        url = reverse('doctor_patient_treatments-list', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        treatment_id = response.data['id']
        url = reverse('doctor_patient_treatments-detail', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id, 'pk': treatment_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment (Modified)'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('doctor_patient_treatments-list', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        treatment_id = response.data['id']
        url = reverse('doctor_patient_treatments-detail', kwargs={'doctor_id': self.doctor_id, 'patient_id': self.patient_id, 'pk': treatment_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
## Testing PatientAssistantView
class PatientAssistantTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
        
        ## Create an assistant
        url_assistants = reverse('assistants-list')
        data = {'name': 'John Doe', 'user': self.user.id}
        response_assistants = self.client.post(url_assistants, data)
        self.assistant_id = response_assistants.data['id']
        
        ## Switch to Doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)      
    
    def test_list(self):
        url = reverse('patient_assistants', kwargs={'pk': self.patient_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('patient_assistants', kwargs={'pk': self.patient_id})
        data = {'assistants': [self.assistant_id]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update(self):
        url = reverse('patient_assistants', kwargs={'pk': self.patient_id})
        data = {'assistants': [self.assistant_id]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete(self):
        url = reverse('patient_assistants', kwargs={'pk': self.patient_id})
        data = {'assistants': [self.assistant_id]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'assistants': []}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
## Testing TreatmentAssistantView
class TreatmentAssistantTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
        
        ## Create a treatment
        url_treatments = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response_treatments = self.client.post(url_treatments, data)
        self.treatment_id = response_treatments.data['id']
        
        ## Create an assistant
        url_assistants = reverse('assistants-list')
        data = {'name': 'John Doe', 'user': self.user.id}
        response_assistants = self.client.post(url_assistants, data)
        self.assistant_id = response_assistants.data['id']
        
        ## Create second assistant
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Assistant')
        data = {'name': 'John Doe 2', 'user': self.user.id}
        response_assistants = self.client.post(url_assistants, data)
        self.assistant_id2 = response_assistants.data['id']
        
        ## Switch to Assistant permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        self.user = User.objects.create_user(username='testuser3', password='testpass')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('treatment_assistant', kwargs={'pk': self.treatment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('treatment_assistant', kwargs={'pk': self.treatment_id})
        data = {'assistant': self.assistant_id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update(self):
        url = reverse('treatment_assistant', kwargs={'pk': self.treatment_id})
        data = {'assistant': self.assistant_id2}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
## Testing PatientTreatmentsReportView
class PatientTreatmentsReportTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
        
        ## Create a treatment
        url_treatments = reverse('treatments-list')
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response_treatments = self.client.post(url_treatments, data)
        self.treatment_id = response_treatments.data['id']
        
        ## Switch to Doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list(self):
        url = reverse('patient_treatments_report-list', kwargs={'patient_id': self.patient_id})
        response_list = self.client.get(url)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        
    def test_create(self):
        url = reverse('patient_treatments_report-list', kwargs={'patient_id': self.patient_id})
        data = {'name': 'Root Canal', 'patient': self.patient_id, 'description': 'Root canal treatment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
## Testing DoctorsPatientsReportView
class DoctorsPatientsReportTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='General Manager')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        ## Create a doctor
        url_doctors = reverse('doctors-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response_doctors = self.client.post(url_doctors, data)
        self.doctor_id = response_doctors.data['id']
        
        ## Create a patient
        url_patients = reverse('patients-list')
        data = {'name': 'John Doe', 'age': 30, 'doctor': self.doctor_id}
        response_patients = self.client.post(url_patients, data)
        self.patient_id = response_patients.data['id']
    
    def test_list(self):
        url = reverse('report-list')
        response_list = self.client.get(url)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        
    def test_create(self):
        url = reverse('report-list')
        data = {'name': 'Dr. John', 'specialization': 'Dentist', 'user': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_report_statistics(self):
        url = reverse('report-list')
        response = self.client.get(url)

        # Check that the response data has a 'statistics' section
        self.assertIn('statistics', response.data)

        # Check that the 'statistics' section has the correct keys
        statistics = response.data['statistics']
        self.assertIn('total_patients', statistics)
        self.assertIn('avg_patients_per_doctor', statistics)

        self.assertEqual(statistics['total_patients'], 1)
        self.assertEqual(statistics['avg_patients_per_doctor'], 1)
        
    def test_list_doctor(self):
        ## Switch to Doctor permissions
        general_manager_group = Group.objects.get(name='General Manager')
        general_manager_group.user_set.remove(self.user)
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.group = Group.objects.create(name='Doctor')
        self.group.user_set.add(self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        url = reverse('report-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
