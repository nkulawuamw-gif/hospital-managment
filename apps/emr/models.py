from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.appointments.models import Appointment


class ICDCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'icd_codes'

    def __str__(self):
        return f'{self.code} - {self.description[:50]}'


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations', limit_choices_to={'role': 'doctor'})
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation')
    chief_complaint = models.TextField()
    symptoms = models.TextField(blank=True, help_text='JSON array of symptoms')
    diagnosis = models.TextField(blank=True)
    icd_codes = models.ManyToManyField(ICDCode, blank=True, related_name='consultations')
    treatment_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'consultations'

    def __str__(self):
        return f'Consultation - {self.patient.patient_id} on {self.created_at.date()}'


class SOAPNote(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='soap_note')
    subjective = models.TextField(blank=True, help_text='Subjective findings from patient')
    objective = models.TextField(blank=True, help_text='Objective clinical findings')
    assessment = models.TextField(blank=True, help_text='Assessment and diagnosis')
    plan = models.TextField(blank=True, help_text='Treatment plan')

    class Meta:
        db_table = 'soap_notes'

    def __str__(self):
        return f'SOAP - Consultation {self.consultation.id}'


class Attachment(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'attachments'

    def __str__(self):
        return f'Attachment for Consultation {self.consultation.id}'
