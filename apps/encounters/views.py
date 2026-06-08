from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count, Sum, F, Prefetch
from django.utils import timezone
from .models import PatientVisit, Encounter, EncounterMedication
from apps.doctors.models import StaffDepartment


@login_required
def active_visits(request):
    visits = PatientVisit.objects.filter(status=PatientVisit.Status.ACTIVE).select_related(
        'patient', 'created_by'
    ).prefetch_related(
        Prefetch(
            'encounters',
            queryset=Encounter.objects.filter(status=Encounter.Status.PENDING),
            to_attr='pending_encounters'
        )
    )
    departments = StaffDepartment.objects.filter(is_active=True)
    context = {
        'visits': visits,
        'departments': departments,
    }
    return render(request, 'encounters/active_visits.html', context)


@login_required
def completed_visits(request):
    visits = PatientVisit.objects.filter(
        status__in=[PatientVisit.Status.COMPLETED, PatientVisit.Status.BILLED]
    ).select_related('patient', 'created_by')
    context = {'visits': visits}
    return render(request, 'encounters/completed_visits.html', context)


@login_required
def start_visit(request, patient_id):
    from patients.models import Patient
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        department_id = request.POST.get('department')
        if not department_id:
            messages.error(request, 'Please select a department to refer to.')
            return redirect('patients:detail', pk=patient_id)
        department = get_object_or_404(StaffDepartment, id=department_id)
        visit = PatientVisit.objects.create(
            patient=patient,
            created_by=request.user
        )
        Encounter.objects.create(
            visit=visit,
            department=department,
            referred_by=request.user,
            status=Encounter.Status.PENDING
        )
        messages.success(request, f'Visit {visit.visit_number} started and referred to {department.name}.')
        return redirect('encounters:active_visits')
    return redirect('patients:detail', pk=patient_id)


@login_required
def department_queue(request):
    user = request.user
    department = user.department
    if not department and user.role not in ['super_admin', 'hospital_admin']:
        messages.error(request, 'You are not assigned to any department.')
        return redirect('dashboard:dashboard')

    if user.role in ['super_admin', 'hospital_admin']:
        encounters = Encounter.objects.all()
    else:
        encounters = Encounter.objects.filter(department=department)

    pending = encounters.filter(status=Encounter.Status.PENDING).select_related(
        'visit__patient', 'referred_from__department'
    )
    in_progress = encounters.filter(status=Encounter.Status.IN_PROGRESS).select_related(
        'visit__patient', 'referred_from__department'
    )

    context = {
        'pending': pending,
        'in_progress': in_progress,
        'department': department,
    }
    return render(request, 'encounters/department_queue.html', context)


@login_required
def encounter_detail(request, pk):
    encounter = get_object_or_404(
        Encounter.objects.select_related(
            'visit__patient', 'department', 'seen_by', 'referred_from__department'
        ).prefetch_related('medications__medicine'),
        pk=pk
    )
    departments = StaffDepartment.objects.filter(is_active=True).exclude(id=encounter.department_id)
    context = {
        'encounter': encounter,
        'departments': departments,
    }
    return render(request, 'encounters/encounter_detail.html', context)


@login_required
def start_encounter(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if encounter.status != Encounter.Status.PENDING:
        messages.error(request, 'This encounter has already been started.')
        return redirect('encounters:department_queue')

    encounter.status = Encounter.Status.IN_PROGRESS
    encounter.seen_by = request.user
    encounter.save()
    messages.success(request, f'Encounter in {encounter.department.name} started.')
    return redirect('encounters:encounter_detail', pk=encounter.pk)


@login_required
@transaction.atomic
def complete_encounter(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if encounter.status != Encounter.Status.IN_PROGRESS:
        messages.error(request, 'This encounter is not in progress.')
        return redirect('encounters:department_queue')

    if request.method == 'POST':
        encounter.chief_complaint = request.POST.get('chief_complaint', '')
        encounter.assessment = request.POST.get('assessment', '')
        encounter.intervention = request.POST.get('intervention', '')
        encounter.notes = request.POST.get('notes', '')

        medicine_ids = request.POST.getlist('medicine_id[]')
        medicine_names = request.POST.getlist('medicine_name[]')
        units = request.POST.getlist('unit[]')
        quantities = request.POST.getlist('quantity[]')
        dosages = request.POST.getlist('dosage[]')
        unit_prices = request.POST.getlist('unit_price[]')

        for i in range(len(quantities)):
            if not quantities[i]:
                continue
            qty_val = quantities[i]
            try:
                qty = int(qty_val)
            except (ValueError, TypeError):
                continue
            if qty <= 0:
                continue

            from pharmacy.models import Medicine
            med_id = medicine_ids[i] if i < len(medicine_ids) else ''
            med_name = medicine_names[i] if i < len(medicine_names) else ''
            unit_price = unit_prices[i] if i < len(unit_prices) else 0

            if med_id and not med_id.startswith('new:'):
                medicine = Medicine.objects.get(id=med_id)
            elif med_name:
                unit = units[i] if i < len(units) else 'other'
                medicine, _ = Medicine.objects.get_or_create(
                    name=med_name,
                    defaults={
                        'unit': unit if unit else 'other',
                        'selling_price': unit_price or 0,
                        'is_active': True,
                    }
                )
            else:
                continue

            EncounterMedication.objects.create(
                encounter=encounter,
                medicine=medicine,
                quantity=qty,
                dosage=dosages[i] if i < len(dosages) else '',
                unit_price=unit_price or medicine.selling_price,
            )

        encounter.status = Encounter.Status.COMPLETED
        encounter.save()

        referred_to_id = request.POST.get('refer_to_department')
        if referred_to_id:
            dept = StaffDepartment.objects.get(id=referred_to_id)
            Encounter.objects.create(
                visit=encounter.visit,
                department=dept,
                referred_from=encounter,
                referred_by=request.user,
                status=Encounter.Status.PENDING
            )
            messages.success(request, f'Encounter completed. Patient referred to {dept.name}.')
        else:
            encounter.visit.status = PatientVisit.Status.COMPLETED
            encounter.visit.checked_out_at = timezone.now()
            encounter.visit.save()
            messages.success(request, 'Encounter completed. Visit finished.')

        return redirect('encounters:department_queue')

    return redirect('encounters:encounter_detail', pk=pk)


@login_required
def cashier_list(request):
    visits = PatientVisit.objects.filter(
        status=PatientVisit.Status.COMPLETED
    ).select_related('patient').annotate(
        med_count=Count('encounters__medications'),
        total_cost=Sum(F('encounters__medications__unit_price') * F('encounters__medications__quantity'))
    )
    billed = PatientVisit.objects.filter(
        status=PatientVisit.Status.BILLED
    ).select_related('patient')
    context = {
        'visits': visits,
        'billed': billed,
    }
    return render(request, 'encounters/cashier_list.html', context)


@login_required
def cashier_detail(request, pk):
    visit = get_object_or_404(
        PatientVisit.objects.select_related('patient', 'created_by')
        .prefetch_related(
            Prefetch(
                'encounters',
                queryset=Encounter.objects.select_related(
                    'department', 'seen_by'
                ).prefetch_related(
                    Prefetch(
                        'medications',
                        queryset=EncounterMedication.objects.select_related('medicine')
                    )
                )
            )
        ),
        pk=pk
    )
    context = {'visit': visit}
    return render(request, 'encounters/cashier_detail.html', context)


@login_required
def mark_billed(request, pk):
    visit = get_object_or_404(PatientVisit, pk=pk)
    if visit.status != PatientVisit.Status.COMPLETED:
        messages.error(request, 'This visit is not yet completed.')
        return redirect('encounters:cashier_list')
    visit.status = PatientVisit.Status.BILLED
    visit.save()
    messages.success(request, f'Visit {visit.visit_number} marked as billed.')
    return redirect('encounters:cashier_list')
