from rest_framework import serializers
from .models import Patient, MedicalHistory


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'patient_id', 'first_name', 'last_name', 'full_name', 'gender', 'date_of_birth', 'age', 'phone', 'email', 'blood_group', 'is_active', 'created_at']


class PatientDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'national_id', 'phone', 'email', 'address', 'emergency_contact_name', 'emergency_contact_phone', 'blood_group', 'allergies', 'insurance_provider', 'insurance_policy_number', 'photo']