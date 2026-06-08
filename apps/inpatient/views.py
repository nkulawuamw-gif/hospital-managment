from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from rest_framework import viewsets
from .models import Ward, Bed, Admission, Transfer
from .serializers import WardSerializer, BedSerializer, AdmissionSerializer, TransferSerializer
from apps.patients.models import Patient
from apps.accounts.models import User


# ------------------ API Views ------------------

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


# ------------------ Template Views ------------------

@login_required
def ward_list(request):
    wards = Ward.objects.all().select_related('department').order_by('name')
    total_capacity = sum(w.capacity for w in wards)
    total_occupied = sum(w.beds.filter(is_occupied=True).count() for w in wards)
    return render(request, 'inpatient/ward_list.html', {
        'wards': wards,
        'total_capacity': total_capacity,
        'total_occupied': total_occupied,
    })


@login_required
def ward_create(request):
    from apps.doctors.models import StaffDepartment
    departments = StaffDepartment.objects.filter(is_active=True)
    if request.method == 'POST':
        ward = Ward.objects.create(
            name=request.POST.get('name'),
            type=request.POST.get('type', 'general'),
            department_id=request.POST.get('department') or None,
            floor=request.POST.get('floor', ''),
            capacity=request.POST.get('capacity', 10),
            charge_per_day=request.POST.get('charge_per_day', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        bed_count = int(request.POST.get('bed_count', ward.capacity))
        for i in range(1, bed_count + 1):
            Bed.objects.create(ward=ward, bed_number=f'B{i:02d}')
        messages.success(request, f'Ward "{ward.name}" created with {bed_count} beds')
        return redirect('inpatient:wards')
    return render(request, 'inpatient/ward_form.html', {
        'departments': departments, 'is_edit': False, 'ward': None,
    })


@login_required
def ward_edit(request, pk):
    from apps.doctors.models import StaffDepartment
    ward = get_object_or_404(Ward, pk=pk)
    departments = StaffDepartment.objects.filter(is_active=True)
    if request.method == 'POST':
        ward.name = request.POST.get('name')
        ward.type = request.POST.get('type')
        ward.department_id = request.POST.get('department') or None
        ward.floor = request.POST.get('floor', '')
        ward.capacity = request.POST.get('capacity', 10)
        ward.charge_per_day = request.POST.get('charge_per_day', 0)
        ward.is_active = request.POST.get('is_active') == 'on'
        ward.save()
        messages.success(request, 'Ward updated')
        return redirect('inpatient:wards')
    return render(request, 'inpatient/ward_form.html', {
        'ward': ward, 'departments': departments, 'is_edit': True,
    })


@login_required
def admission_list(request):
    status_filter = request.GET.get('status', 'admitted')
    admissions = Admission.objects.all().select_related(
        'patient', 'ward', 'bed', 'doctor', 'created_by'
    ).order_by('-admission_date')
    if status_filter and status_filter != 'all':
        admissions = admissions.filter(status=status_filter)
    counts = {
        'all': Admission.objects.count(),
        'admitted': Admission.objects.filter(status='admitted').count(),
        'discharged': Admission.objects.filter(status='discharged').count(),
        'transferred': Admission.objects.filter(status='transferred').count(),
    }
    return render(request, 'inpatient/admission_list.html', {
        'admissions': admissions,
        'current_status': status_filter,
        'counts': counts,
    })


@login_required
def admission_create(request):
    patients = Patient.objects.filter(is_active=True)
    wards = Ward.objects.filter(is_active=True)
    doctors = User.objects.filter(role='doctor', is_active=True)
    if request.method == 'POST':
        admission = Admission.objects.create(
            patient_id=request.POST.get('patient'),
            ward_id=request.POST.get('ward') or None,
            bed_id=request.POST.get('bed') or None,
            doctor_id=request.POST.get('doctor') or None,
            diagnosis=request.POST.get('diagnosis', ''),
            notes=request.POST.get('notes', ''),
            created_by=request.user,
        )
        if admission.bed:
            admission.bed.is_occupied = True
            admission.bed.save()
        messages.success(request, f'Patient {admission.patient.full_name} admitted to {admission.ward.name if admission.ward else "hospital"}')
        return redirect('inpatient:admission_detail', pk=admission.pk)
    return render(request, 'inpatient/admission_form.html', {
        'patients': patients, 'wards': wards, 'doctors': doctors,
    })


@login_required
def admission_detail(request, pk):
    admission = get_object_or_404(
        Admission.objects.select_related('patient', 'ward', 'bed', 'doctor', 'created_by'),
        pk=pk,
    )
    transfers = admission.transfers.all().select_related('from_ward', 'to_ward', 'transferred_by').order_by('-transferred_at')
    return render(request, 'inpatient/admission_detail.html', {
        'admission': admission, 'transfers': transfers,
    })


@login_required
def admission_transfer(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    wards = Ward.objects.filter(is_active=True)
    if request.method == 'POST':
        to_ward_id = request.POST.get('to_ward') or None
        to_bed_id = request.POST.get('to_bed') or None
        Transfer.objects.create(
            admission=admission,
            from_ward=admission.ward,
            to_ward_id=to_ward_id,
            from_bed=admission.bed,
            to_bed_id=to_bed_id,
            reason=request.POST.get('reason', ''),
            transferred_by=request.user,
        )
        if admission.bed:
            admission.bed.is_occupied = False
            admission.bed.save()
        admission.ward_id = to_ward_id
        admission.bed_id = to_bed_id
        admission.status = Admission.Status.TRANSFERRED
        admission.save()
        if to_bed_id:
            new_bed = Bed.objects.get(pk=to_bed_id)
            new_bed.is_occupied = True
            new_bed.save()
        messages.success(request, 'Patient transferred')
        return redirect('inpatient:admission_detail', pk=pk)
    return render(request, 'inpatient/admission_transfer.html', {
        'admission': admission, 'wards': wards,
    })


@login_required
def admission_discharge(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        admission.status = Admission.Status.DISCHARGED
        admission.discharge_date = datetime.now()
        admission.notes = (admission.notes + '\n\n--- DISCHARGE ---\n' + request.POST.get('discharge_notes', '')).strip()
        admission.save()
        if admission.bed:
            admission.bed.is_occupied = False
            admission.bed.save()
        messages.success(request, f'{admission.patient.full_name} discharged')
        return redirect('inpatient:admission_detail', pk=pk)
    return render(request, 'inpatient/admission_discharge.html', {'admission': admission})
