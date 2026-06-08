from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, MedicalHistory
from .serializers import PatientListSerializer, PatientDetailSerializer, PatientCreateSerializer, MedicalHistorySerializer
from apps.doctors.models import StaffDepartment
from apps.api.utils import generate_patient_id


# ------------------ API Views ------------------

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'national_id']
    ordering_fields = ['created_at', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        if self.action == 'create':
            return PatientCreateSerializer
        return PatientDetailSerializer

    def perform_create(self, serializer):
        serializer.save(patient_id=generate_patient_id(), registered_by=self.request.user)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer


# ------------------ Template Views ------------------

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/list.html', {'patients': patients})


@login_required
def patient_create(request):
    if request.method == 'POST':
        patient = Patient(
            patient_id=generate_patient_id(),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            national_id=request.POST.get('national_id', ''),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            emergency_contact_name=request.POST.get('emergency_contact_name', ''),
            emergency_contact_phone=request.POST.get('emergency_contact_phone', ''),
            blood_group=request.POST.get('blood_group', ''),
            allergies=request.POST.get('allergies', ''),
            insurance_provider=request.POST.get('insurance_provider', ''),
            insurance_policy_number=request.POST.get('insurance_policy_number', ''),
            photo=request.FILES.get('photo'),
            registered_by=request.user,
        )
        patient.save()
        messages.success(request, f'Patient {patient.full_name} registered (ID: {patient.patient_id})')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/form.html', {'is_edit': False})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-appointment_date')[:10]
    consultations = patient.consultations.all().order_by('-created_at')[:10]
    prescriptions = patient.prescriptions.all().order_by('-created_at')[:10]
    invoices = patient.invoices.all().order_by('-created_at')[:10]
    lab_requests = patient.lab_requests.all().order_by('-created_at')[:10]
    admissions = patient.admissions.all().order_by('-admission_date')[:10]
    medical_histories = patient.medical_histories.all()
    visits = patient.visits.all().order_by('-created_at')[:10]
    departments = StaffDepartment.objects.filter(is_active=True)

    context = {
        'patient': patient,
        'appointments': appointments,
        'consultations': consultations,
        'prescriptions': prescriptions,
        'invoices': invoices,
        'lab_requests': lab_requests,
        'admissions': admissions,
        'medical_histories': medical_histories,
        'visits': visits,
        'departments': departments,
    }
    return render(request, 'patients/detail.html', context)


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.gender = request.POST.get('gender')
        patient.date_of_birth = request.POST.get('date_of_birth')
        patient.national_id = request.POST.get('national_id', '')
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email', '')
        patient.address = request.POST.get('address', '')
        patient.emergency_contact_name = request.POST.get('emergency_contact_name', '')
        patient.emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        patient.blood_group = request.POST.get('blood_group', '')
        patient.allergies = request.POST.get('allergies', '')
        patient.insurance_provider = request.POST.get('insurance_provider', '')
        patient.insurance_policy_number = request.POST.get('insurance_policy_number', '')
        patient.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('photo'):
            patient.photo = request.FILES.get('photo')
        patient.save()
        messages.success(request, 'Patient updated')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/form.html', {'patient': patient, 'is_edit': True})


@login_required
def patient_add_medical_history(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        condition = request.POST.get('condition')
        diagnosed_date = request.POST.get('diagnosed_date') or None
        notes = request.POST.get('notes', '')
        MedicalHistory.objects.create(
            patient=patient,
            condition=condition,
            diagnosed_date=diagnosed_date,
            notes=notes,
        )
        messages.success(request, 'Medical history added')
    return redirect('patients:detail', pk=patient.pk)
