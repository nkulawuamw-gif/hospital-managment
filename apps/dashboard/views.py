import re
import json
import secrets
import string
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.urls import reverse

from apps.accounts.models import User
from apps.doctors.models import DoctorProfile
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.inpatient.models import Admission
from apps.billing.models import Invoice, Payment
from apps.pharmacy.models import MedicineBatch
from apps.laboratory.models import LabRequest
from apps.notifications.models import Notification, EmailLog, SMSLog
from .models import (
    HealthArticle, SiteSetting, HeroSection, WhyChooseItem,
    ServiceCategory, Department, MedicalTeam, Testimonial, Statistic, ContactInfo,
)


def landing_view(request):
    site = SiteSetting.get_settings()
    hero = HeroSection.objects.first()

    doctors_qs = DoctorProfile.objects.filter(
        user__is_active=True, is_available=True
    ).select_related('user').prefetch_related('specializations')[:8]

    doctors = []
    for dp in doctors_qs:
        user = dp.user
        specializations = ', '.join([s.name for s in dp.specializations.all()]) if dp.pk else ''
        doctors.append({
            'id': user.pk,
            'full_name': user.get_full_name() or user.email,
            'qualification': dp.qualifications or '',
            'bio': '',
            'specialization': specializations or 'General Practitioner',
            'profile_image': getattr(user, 'profile_picture', None) or None,
        })

    articles = HealthArticle.objects.filter(is_published=True)[:6]

    context = {
        'site': site,
        'hero': hero,
        'doctors': doctors,
        'health_articles': articles,
        'why_choose_items': WhyChooseItem.objects.filter(is_active=True).order_by('order'),
        'service_categories': ServiceCategory.objects.filter(is_active=True).order_by('order').prefetch_related('items'),
        'departments': Department.objects.filter(is_active=True).order_by('order'),
        'medical_teams': MedicalTeam.objects.filter(is_active=True).order_by('order'),
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'statistics': Statistic.objects.filter(is_active=True).order_by('order'),
        'contact_infos': ContactInfo.objects.filter(is_active=True).order_by('order'),
    }
    return render(request, 'landing/index.html', context)


def book_appointment_view(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method != 'POST':
        if is_ajax:
            return JsonResponse({'success': False, 'errors': ['Invalid request method']}, status=400)
        return redirect('dashboard:home')

    full_name = request.POST.get('full_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    service = request.POST.get('service', '').strip()
    preferred_date = request.POST.get('preferred_date', '').strip()
    preferred_time = request.POST.get('preferred_time', '').strip()
    message = request.POST.get('message', '').strip()

    errors = []
    if not full_name:
        errors.append('Full name is required')
    if not phone:
        errors.append('Phone number is required')
    if not service:
        errors.append('Service is required')
    if not preferred_date:
        errors.append('Preferred date is required')

    if errors:
        if is_ajax:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        for err in errors:
            messages.error(request, err)
        return redirect('dashboard:home')

    name_parts = full_name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    phone_clean = re.sub(r'\D', '', phone)
    timestamp = int(timezone.now().timestamp())
    patient_id = f'PUB-{timestamp}'

    patient, created = Patient.objects.get_or_create(
        phone=phone_clean,
        defaults={
            'patient_id': patient_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'gender': 'other',
            'date_of_birth': date(1990, 1, 1),
            'is_active': True,
        }
    )

    first_doctor = User.objects.filter(role='doctor', is_active=True).first()
    if first_doctor is None:
        first_doctor = User.objects.filter(role__in=['super_admin', 'hospital_admin'], is_active=True).first()

    appointment = Appointment.objects.create(
        patient=patient,
        doctor=first_doctor,
        appointment_date=preferred_date,
        appointment_time=preferred_time or None,
        reason=f'{service}: {message}' if message else service,
        status='scheduled',
        source=Appointment.Source.WEB,
        notes=f'Booked via public website by {full_name} ({phone}{", " + email if email else ""}).',
    )

    appointment_detail_url = reverse('appointments:detail', args=[appointment.pk])
    recipients = User.objects.filter(
        role__in=['super_admin', 'hospital_admin', 'receptionist'],
        is_active=True,
    )
    if first_doctor:
        recipients = (recipients | User.objects.filter(pk=first_doctor.pk)).distinct()
    else:
        recipients = recipients.distinct()

    preferred_time_display = preferred_time if preferred_time else 'any time'
    note = (f' Notes: {message}' if message else '')
    for recipient in recipients:
        Notification.objects.create(
            recipient=recipient,
            type=Notification.Type.APPOINTMENT,
            title=f'New website booking from {full_name}',
            message=(
                f'{full_name} ({phone}) requested an appointment for {service} '
                f'on {preferred_date} at {preferred_time_display}.{note}'
            ),
            link=appointment_detail_url,
        )

    patient_user = None
    if email:
        patient_user, user_created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': User.Role.PATIENT,
                'phone': phone,
                'is_active': True,
            },
        )
        if user_created:
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(10))
            patient_user.set_password(temp_password)
            patient_user.save()
            patient_user.temporary_password = temp_password
        else:
            patient_user.temporary_password = None
            if not patient_user.phone:
                patient_user.phone = phone
                patient_user.save(update_fields=['phone'])

        Notification.objects.create(
            recipient=patient_user,
            type=Notification.Type.APPOINTMENT,
            title='Your appointment request was received',
            message=(
                f'Dear {full_name}, your request for {service} on '
                f'{preferred_date} at {preferred_time_display} has been received. '
                f'Reference: {patient.patient_id}. Our team will contact you at {phone} to confirm.'
            ),
            link=reverse('appointments:detail', args=[appointment.pk]),
        )

    email_body = (
        f'Dear {full_name},\n\n'
        f'Your appointment request for {service} on {preferred_date} '
        f'at {preferred_time_display} has been received.\n'
        f'Reference: {patient.patient_id}\n\n'
    )
    if patient_user is not None and getattr(patient_user, 'temporary_password', None):
        email_body += (
            f'A patient portal account has been created for you.\n'
            f'Login: {email}\n'
            f'Temporary password: {patient_user.temporary_password}\n'
            f'Please change your password after first login.\n\n'
        )
    email_body += 'We will contact you at ' + phone + ' to confirm.\n\n-- Hope Clinic'

    if email:
        try:
            EmailLog.objects.create(
                recipient=email,
                subject='Hope Clinic - Appointment Request Received',
                body=email_body,
                status='sent',
            )
        except Exception:
            pass

    try:
        SMSLog.objects.create(
            recipient=phone_clean,
            message=(
                f'Hope Clinic: Your appointment request for {service} on '
                f'{preferred_date} has been received. Ref: {patient.patient_id}. '
                f'We will call to confirm.'
            ),
            status='sent',
        )
    except Exception:
            pass

    success_message = (
        f'Appointment request submitted successfully! '
        f'Your reference: {patient.patient_id}. We will contact you at {phone}.'
    )
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': success_message,
            'reference': patient.patient_id,
            'appointment_id': appointment.pk,
        })
    messages.success(request, success_message)
    return redirect('dashboard:home')


@login_required
def dashboard_view(request):
    today = date.today()
    first_of_month = today.replace(day=1)

    patient_count = Patient.objects.filter(is_active=True).count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    admitted = Admission.objects.filter(status='admitted').count()
    discharged = Admission.objects.filter(status='discharged').count()

    revenue_today = Payment.objects.filter(
        payment_date__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    revenue_month = Payment.objects.filter(
        payment_date__date__gte=first_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    low_stock = MedicineBatch.objects.filter(
        quantity_remaining__lte=models.F('medicine__reorder_level')
    ).count()

    pending_lab = LabRequest.objects.filter(status='pending').count()

    upcoming = Appointment.objects.filter(
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')[:10]

    unread_notifications = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).count()

    context = {
        'patient_count': patient_count,
        'today_appointments': today_appointments,
        'admitted': admitted,
        'discharged': discharged,
        'revenue_today': revenue_today,
        'revenue_month': revenue_month,
        'low_stock': low_stock,
        'pending_lab': pending_lab,
        'upcoming_appointments': upcoming,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'dashboard/index.html', context)
