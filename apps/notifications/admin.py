from django.contrib import admin
from .models import Notification, EmailLog, SMSLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'type', 'title', 'is_read', 'created_at']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    pass

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    pass