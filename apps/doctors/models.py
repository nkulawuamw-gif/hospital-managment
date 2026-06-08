from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class StaffDepartment(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departments'
        verbose_name = 'Staff Department'
        verbose_name_plural = 'Staff Departments'

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'specializations'

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(StaffDepartment, on_delete=models.SET_NULL, null=True, related_name='doctors')
    specializations = models.ManyToManyField(Specialization, related_name='doctors')
    license_number = models.CharField(max_length=100, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qualifications = models.TextField(blank=True, help_text='Qualifications, comma separated')
    available_days = models.CharField(max_length=200, blank=True, help_text='Comma separated: Monday,Tuesday,Wednesday,Thursday,Friday,Saturday')
    available_from = models.TimeField(default='08:00')
    available_to = models.TimeField(default='17:00')
    max_patients_per_day = models.IntegerField(default=20)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'doctor_profiles'

    def __str__(self):
        return f'Dr. {self.user.get_full_name()} - {self.department}'


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules', limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    reason_unavailable = models.TextField(blank=True)

    class Meta:
        db_table = 'doctor_schedules'
        unique_together = ['doctor', 'date']

    def __str__(self):
        return f'{self.doctor.get_full_name()} - {self.date}'
