from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPER_ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        HOSPITAL_ADMIN = 'hospital_admin', 'Hospital Administrator'
        DOCTOR = 'doctor', 'Doctor'
        NURSE = 'nurse', 'Nurse'
        RECEPTIONIST = 'receptionist', 'Receptionist'
        PHARMACIST = 'pharmacist', 'Pharmacist'
        LAB_TECHNICIAN = 'lab_technician', 'Laboratory Technician'
        CASHIER = 'cashier', 'Cashier'
        ACCOUNTANT = 'accountant', 'Accountant'
        PATIENT = 'patient', 'Patient'

    username = None
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    department = models.ForeignKey('doctors.StaffDepartment', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    history = HistoricalRecords()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'

    @property
    def full_name(self):
        return self.get_full_name()


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions')
    can_manage_patients = models.BooleanField(default=False)
    can_manage_appointments = models.BooleanField(default=False)
    can_manage_billing = models.BooleanField(default=False)
    can_manage_pharmacy = models.BooleanField(default=False)
    can_manage_lab = models.BooleanField(default=False)
    can_manage_inventory = models.BooleanField(default=False)
    can_manage_hr = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_permissions'

    def __str__(self):
        return f'Permissions for {self.user.email}'


class Module(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, default='bi bi-circle')
    url_name = models.CharField(max_length=200, blank=True)
    section = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'modules'
        ordering = ['section', 'order']

    def __str__(self):
        return self.name


class RoleModulePermission(models.Model):
    role = models.CharField(max_length=20, choices=User.Role.choices, unique=True)
    modules = models.ManyToManyField(Module)

    class Meta:
        db_table = 'role_module_permissions'
        verbose_name = 'Role Module Permission'

    def __str__(self):
        return dict(User.Role.choices).get(self.role, self.role)
