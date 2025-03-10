# patients/serializers.py
from rest_framework import serializers
from .models import Patient, HealthInsurance

class HealthInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurance
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    health_insurance_detail = HealthInsuranceSerializer(source='health_insurance', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'