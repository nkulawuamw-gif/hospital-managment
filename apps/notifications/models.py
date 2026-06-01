from django.db import models
from apps.accounts.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        APPOINTMENT = 'appointment', 'Appointment'
        BILLING = 'billing', 'Billing'
        PHARMACY = 'pharmacy', 'Pharmacy'
        LAB = 'lab', 'Laboratory'
        SYSTEM = 'system', 'System'
        REMINDER = 'reminder', 'Reminder'

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    title = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, help_text='URL to navigate to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f'{self.recipient.email} - {self.title[:50]}'


class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=500)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'email_logs'


class SMSLog(models.Model):
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'sms_logs'
