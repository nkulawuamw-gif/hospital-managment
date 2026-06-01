from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        CONFIRMED = 'confirmed', 'Confirmed'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'doctor'})
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_out_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'appointments'
        indexes = [
            models.Index(fields=['appointment_date']),
            models.Index(fields=['status']),
            models.Index(fields=['doctor', 'appointment_date']),
        ]

    def __str__(self):
        return f'{self.patient.patient_id} - Dr. {self.doctor.last_name} - {self.appointment_date}'


class AppointmentReminder(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    sent_via = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS')])
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')

    class Meta:
        db_table = 'appointment_reminders'
