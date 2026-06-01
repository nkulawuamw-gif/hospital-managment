from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import ICDCode, Consultation, SOAPNote, Attachment
from .serializers import ICDCodeSerializer, ConsultationSerializer, ConsultationCreateSerializer, SOAPNoteSerializer, AttachmentSerializer
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.accounts.models import User


# ------------------ API Views ------------------

class ICDCodeViewSet(viewsets.ModelViewSet):
    queryset = ICDCode.objects.all()
    serializer_class = ICDCodeSerializer
    search_fields = ['code', 'description']


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ConsultationCreateSerializer
        return ConsultationSerializer


class SOAPNoteViewSet(viewsets.ModelViewSet):
    queryset = SOAPNote.objects.all()
    serializer_class = SOAPNoteSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# ------------------ Template Views ------------------

@login_required
def consultation_list(request):
    consultations = Consultation.objects.all().order_by('-created_at')
    doctor_filter = request.GET.get('doctor', '')
    if doctor_filter:
        consultations = consultations.filter(doctor_id=doctor_filter)
    doctors = User.objects.filter(role='doctor', is_active=True)
    return render(request, 'emr/list.html', {
        'consultations': consultations,
        'doctors': doctors,
        'current_doctor': doctor_filter,
    })


@login_required
def consultation_create(request):
    patients = Patient.objects.filter(is_active=True)
    doctors = User.objects.filter(role='doctor', is_active=True)
    icd_codes = ICDCode.objects.all()
    appointments = Appointment.objects.filter(
        status='in_progress',
        doctor=request.user if request.user.role == 'doctor' else None
    ) if request.user.role == 'doctor' else Appointment.objects.filter(status='in_progress')

    if request.method == 'POST':
        consultation = Consultation.objects.create(
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor', request.user.pk if request.user.role == 'doctor' else None),
            appointment_id=request.POST.get('appointment') or None,
            chief_complaint=request.POST.get('chief_complaint'),
            symptoms=request.POST.get('symptoms', ''),
            diagnosis=request.POST.get('diagnosis', ''),
            treatment_plan=request.POST.get('treatment_plan', ''),
            notes=request.POST.get('notes', ''),
            follow_up_date=request.POST.get('follow_up_date') or None,
        )
        icd_ids = request.POST.getlist('icd_codes')
        if icd_ids:
            consultation.icd_codes.set(icd_ids)

        subjective = request.POST.get('subjective', '')
        objective = request.POST.get('objective', '')
        assessment = request.POST.get('assessment', '')
        plan = request.POST.get('plan', '')
        if any([subjective, objective, assessment, plan]):
            SOAPNote.objects.create(
                consultation=consultation,
                subjective=subjective,
                objective=objective,
                assessment=assessment,
                plan=plan,
            )

        messages.success(request, 'Consultation recorded')
        return redirect('emr:detail', pk=consultation.pk)

    return render(request, 'emr/form.html', {
        'patients': patients,
        'doctors': doctors,
        'icd_codes': icd_codes,
        'appointments': appointments,
    })


@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'emr/detail.html', {'c': consultation})
