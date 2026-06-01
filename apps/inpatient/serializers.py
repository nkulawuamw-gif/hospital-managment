from rest_framework import serializers
from .models import Ward, Bed, Admission, Transfer


class WardSerializer(serializers.ModelSerializer):
    available_beds = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ward
        fields = '__all__'


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'


class AdmissionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = Admission
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'