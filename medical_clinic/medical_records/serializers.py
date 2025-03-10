from rest_framework import serializers
from .models import MedicalRecord, Prescription, ExamRequest
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from appointments.serializers import AppointmentSerializer

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class ExamRequestSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ExamRequest
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    appointment_detail = AppointmentSerializer(source='appointment', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    exam_requests = ExamRequestSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'