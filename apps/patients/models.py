from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    class BloodGroup(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=5, choices=BloodGroup.choices, blank=True)
    allergies = models.TextField(blank=True, help_text='Known allergies (comma separated)')
    insurance_provider = models.CharField(max_length=200, blank=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='patients/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'patients'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['national_id']),
        ]

    def __str__(self):
        return f'{self.patient_id} - {self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return 0


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition = models.CharField(max_length=300)
    diagnosed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medical_histories'

    def __str__(self):
        return f'{self.patient.patient_id} - {self.condition}'
