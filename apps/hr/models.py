from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class Employee(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        CONTRACT = 'contract', 'Contract'
        INTERN = 'intern', 'Intern'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    date_joined = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    emergency_contact = models.CharField(max_length=200, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f'{self.employee_id} - {self.user.get_full_name()}'


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    is_present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'attendance'
        unique_together = ['employee', 'date']

    def __str__(self):
        return f'{self.employee.employee_id} - {self.date}'


class Leave(models.Model):
    class Type(models.TextChoices):
        ANNUAL = 'annual', 'Annual Leave'
        SICK = 'sick', 'Sick Leave'
        MATERNITY = 'maternity', 'Maternity Leave'
        PATERNITY = 'paternity', 'Paternity Leave'
        UNPAID = 'unpaid', 'Unpaid Leave'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=Type.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaves'

    def __str__(self):
        return f'{self.employee.employee_id} - {self.get_leave_type_display()}'
