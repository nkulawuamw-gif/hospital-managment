from django.contrib import admin
from .models import ICDCode, Consultation, SOAPNote, Attachment

@admin.register(ICDCode)
class ICDCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    search_fields = ['code', 'description']

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'created_at']

@admin.register(SOAPNote)
class SOAPNoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass