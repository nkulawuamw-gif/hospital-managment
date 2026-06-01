from rest_framework import serializers
from .models import InsuranceCompany, PatientInsurance, InsuranceClaim


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'


class PatientInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInsurance
        fields = '__all__'


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'