from rest_framework import serializers
from .models import ICDCode, Consultation, SOAPNote, Attachment


class ICDCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICDCode
        fields = '__all__'


class SOAPNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOAPNote
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    soap_note = SOAPNoteSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'


class ConsultationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'appointment', 'chief_complaint', 'symptoms', 'diagnosis', 'icd_codes', 'treatment_plan', 'notes', 'follow_up_date']