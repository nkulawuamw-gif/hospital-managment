from rest_framework import serializers
from .models import Appointment, AppointmentReminder


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'reason']


class AppointmentReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReminder
        fields = '__all__'