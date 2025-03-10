# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment, Notification
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    notifications = NotificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'