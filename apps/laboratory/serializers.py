from rest_framework import serializers
from .models import LabTestCategory, LabTest, LabTestParameter, LabRequest, LabRequestItem, LabResultParameter


class LabTestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestCategory
        fields = '__all__'


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'


class LabTestParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestParameter
        fields = '__all__'


class LabRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRequest
        fields = '__all__'


class LabRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRequestItem
        fields = '__all__'


class LabResultParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResultParameter
        fields = '__all__'