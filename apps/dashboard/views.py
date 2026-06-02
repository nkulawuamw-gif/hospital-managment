import re
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone

from apps.accounts.models import User
from apps.doctors.models import DoctorProfile
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.inpatient.models import Admission
from apps.billing.models import Invoice, Payment
from apps.pharmacy.models import MedicineBatch
from apps.laboratory.models import LabRequest
from apps.notifications.models import Notification
from .models import (
    HealthArticle, SiteSetting, HeroSection, WhyChooseItem,
    ServiceCategory, Department, Testimonial, Statistic, ContactInfo,
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
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'statistics': Statistic.objects.filter(is_active=True).order_by('order'),
        'contact_infos': ContactInfo.objects.filter(is_active=True).order_by('order'),
    }
    return render(request, 'landing/index.html', context)


def book_appointment_view(request):
    if request.method != 'POST':
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

    appointment = Appointment.objects.create(
        patient=patient,
        doctor=first_doctor,
        appointment_date=preferred_date,
        appointment_time=preferred_time or None,
        reason=f'{service}: {message}' if message else service,
        status='scheduled',
    )

    messages.success(
        request,
        f'Appointment request submitted successfully! Your reference: {patient.patient_id}. We will contact you at {phone}.'
    )
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
