# doctors/serializers.py
from rest_framework import serializers
from .models import Doctor, Specialty, DoctorSchedule

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

class DoctorScheduleSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'weekday', 'weekday_display', 'start_time', 'end_time']

class DoctorSerializer(serializers.ModelSerializer):
    specialties_detail = SpecialtySerializer(source='specialties', many=True, read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'