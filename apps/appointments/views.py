from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment, AppointmentReminder
from .serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentReminderSerializer
from apps.patients.models import Patient
from apps.accounts.models import User


# ------------------ API Views ------------------

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_date', 'doctor']
    search_fields = ['patient__first_name', 'patient__patient_id']

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        apt = self.get_object()
        apt.status = Appointment.Status.IN_PROGRESS
        apt.checked_in_at = datetime.now()
        apt.save()
        return Response({'message': 'Patient checked in'})

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        apt = self.get_object()
        apt.status = Appointment.Status.COMPLETED
        apt.checked_out_at = datetime.now()
        apt.save()
        return Response({'message': 'Patient checked out'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        apt = self.get_object()
        apt.status = Appointment.Status.CANCELLED
        apt.save()
        return Response({'message': 'Appointment cancelled'})


# ------------------ Template Views ------------------

@login_required
def appointment_list(request):
    today = date.today()
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    source_filter = request.GET.get('source', '')

    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    if source_filter:
        appointments = appointments.filter(source=source_filter)

    status_counts = Appointment.objects.values('status').annotate(count=Count('id'))
    stats = {s['status']: s['count'] for s in status_counts}

    source_counts = dict(
        Appointment.objects.values_list('source').annotate(count=Count('id')).order_by()
    )
    source_stats = {s: source_counts.get(s, 0) for s, _ in Appointment.Source.choices}

    context = {
        'appointments': appointments,
        'stats': stats,
        'source_stats': source_stats,
        'source_choices': Appointment.Source.choices,
        'today': today,
        'current_status': status_filter,
        'current_date': date_filter,
        'current_source': source_filter,
    }
    return render(request, 'appointments/list.html', context)


@login_required
def appointment_create(request):
    patients = Patient.objects.filter(is_active=True).order_by('first_name')
    doctors = User.objects.filter(role='doctor', is_active=True).order_by('first_name')

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        apt_date = request.POST.get('appointment_date')
        apt_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason', '')

        try:
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=apt_date,
                appointment_time=apt_time,
                reason=reason,
                created_by=request.user,
            )
            messages.success(request, f'Appointment booked for {appointment.patient.full_name}')
            return redirect('appointments:list')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    context = {
        'patients': patients,
        'doctors': doctors,
    }
    return render(request, 'appointments/form.html', context)


@login_required
def appointment_detail(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/detail.html', {'apt': apt})


@login_required
def appointment_checkin(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    if apt.status not in ('scheduled', 'confirmed'):
        messages.warning(request, 'Appointment cannot be checked in')
    else:
        apt.status = Appointment.Status.IN_PROGRESS
        apt.checked_in_at = datetime.now()
        apt.save()
        messages.success(request, f'{apt.patient.full_name} checked in')
    return redirect('appointments:detail', pk=pk)


@login_required
def appointment_checkout(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    if apt.status != 'in_progress':
        messages.warning(request, 'Appointment must be in progress to check out')
    else:
        apt.status = Appointment.Status.COMPLETED
        apt.checked_out_at = datetime.now()
        apt.save()
        messages.success(request, f'{apt.patient.full_name} checked out')
    return redirect('appointments:detail', pk=pk)


@login_required
def appointment_cancel(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    apt.status = Appointment.Status.CANCELLED
    apt.save()
    messages.success(request, 'Appointment cancelled')
    return redirect('appointments:list')


@login_required
def calendar_view(request):
    appointments = Appointment.objects.filter(
        appointment_date__gte=date.today(),
        status__in=['scheduled', 'confirmed', 'in_progress']
    ).order_by('appointment_date', 'appointment_time')
    return render(request, 'appointments/calendar.html', {'appointments': appointments})
