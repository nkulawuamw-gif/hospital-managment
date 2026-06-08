from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets
from .models import StaffDepartment, Specialization, DoctorProfile, DoctorSchedule
from .serializers import DepartmentSerializer, SpecializationSerializer, DoctorProfileSerializer, DoctorScheduleSerializer
from apps.accounts.models import User


# ------------------ API Views ------------------

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = StaffDepartment.objects.all()
    serializer_class = DepartmentSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer


# ------------------ Template Views ------------------

@login_required
def department_list(request):
    depts = StaffDepartment.objects.all().order_by('name')
    return render(request, 'doctors/department_list.html', {'departments': depts})


@login_required
def department_create(request):
    if request.method == 'POST':
        StaffDepartment.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            location=request.POST.get('location', ''),
            phone=request.POST.get('phone', ''),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Department created')
        return redirect('doctors:departments')
    return render(request, 'doctors/department_form.html', {'is_edit': False, 'dept': None})


@login_required
def department_edit(request, pk):
    dept = get_object_or_404(StaffDepartment, pk=pk)
    if request.method == 'POST':
        dept.name = request.POST.get('name')
        dept.description = request.POST.get('description', '')
        dept.location = request.POST.get('location', '')
        dept.phone = request.POST.get('phone', '')
        dept.is_active = request.POST.get('is_active') == 'on'
        dept.save()
        messages.success(request, 'Department updated')
        return redirect('doctors:departments')
    return render(request, 'doctors/department_form.html', {'dept': dept, 'is_edit': True})


@login_required
def specialization_list(request):
    specs = Specialization.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        desc = request.POST.get('description', '').strip()
        if name:
            Specialization.objects.get_or_create(name=name, defaults={'description': desc})
            messages.success(request, f'Specialization "{name}" added')
        return redirect('doctors:specializations')
    return render(request, 'doctors/specialization_list.html', {'specializations': specs})


@login_required
def doctor_list(request):
    dept_filter = request.GET.get('department', '')
    search = request.GET.get('q', '')
    doctors = DoctorProfile.objects.all().select_related('user', 'department').prefetch_related('specializations').order_by('user__last_name')
    if dept_filter:
        doctors = doctors.filter(department_id=dept_filter)
    if search:
        doctors = doctors.filter(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(license_number__icontains=search))
    departments = StaffDepartment.objects.filter(is_active=True)
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors, 'departments': departments,
        'current_dept': dept_filter, 'search': search,
    })


@login_required
def doctor_detail(request, pk):
    profile = get_object_or_404(
        DoctorProfile.objects.select_related('user', 'department').prefetch_related('specializations', 'user__schedules'),
        pk=pk,
    )
    upcoming_schedules = profile.user.schedules.filter(date__gte=__import__('datetime').date.today()).order_by('date')[:14]
    return render(request, 'doctors/doctor_detail.html', {
        'profile': profile, 'upcoming_schedules': upcoming_schedules,
    })


@login_required
def doctor_create(request):
    departments = StaffDepartment.objects.filter(is_active=True)
    specs = Specialization.objects.all()
    if request.method == 'POST':
        # Create user account first
        email = request.POST.get('email')
        first = request.POST.get('first_name')
        last = request.POST.get('last_name')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', 'changeme123')
        user = User.objects.create_user(
            email=email, password=password,
            first_name=first, last_name=last, phone=phone, role='doctor',
        )
        profile = DoctorProfile.objects.create(
            user=user,
            department_id=request.POST.get('department') or None,
            license_number=request.POST.get('license_number'),
            consultation_fee=request.POST.get('consultation_fee', 0),
            qualifications=request.POST.get('qualifications', ''),
            available_days=request.POST.get('available_days', 'Monday,Tuesday,Wednesday,Thursday,Friday'),
            available_from=request.POST.get('available_from', '08:00'),
            available_to=request.POST.get('available_to', '17:00'),
            max_patients_per_day=request.POST.get('max_patients_per_day', 20),
            is_available=request.POST.get('is_available') == 'on',
        )
        spec_ids = request.POST.getlist('specializations')
        if spec_ids:
            profile.specializations.set(spec_ids)
        messages.success(request, f'Dr. {user.get_full_name()} added (default password: {password})')
        return redirect('doctors:doctor_detail', pk=profile.pk)
    return render(request, 'doctors/doctor_form.html', {
        'departments': departments, 'specializations': specs, 'is_edit': False, 'profile': None,
    })


@login_required
def doctor_edit(request, pk):
    profile = get_object_or_404(DoctorProfile, pk=pk)
    departments = StaffDepartment.objects.filter(is_active=True)
    specs = Specialization.objects.all()
    if request.method == 'POST':
        profile.user.first_name = request.POST.get('first_name')
        profile.user.last_name = request.POST.get('last_name')
        profile.user.phone = request.POST.get('phone', '')
        profile.user.save()
        profile.department_id = request.POST.get('department') or None
        profile.license_number = request.POST.get('license_number')
        profile.consultation_fee = request.POST.get('consultation_fee', 0)
        profile.qualifications = request.POST.get('qualifications', '')
        profile.available_days = request.POST.get('available_days', '')
        profile.available_from = request.POST.get('available_from', '08:00')
        profile.available_to = request.POST.get('available_to', '17:00')
        profile.max_patients_per_day = request.POST.get('max_patients_per_day', 20)
        profile.is_available = request.POST.get('is_available') == 'on'
        profile.save()
        profile.specializations.set(request.POST.getlist('specializations'))
        messages.success(request, 'Doctor profile updated')
        return redirect('doctors:doctor_detail', pk=profile.pk)
    return render(request, 'doctors/doctor_form.html', {
        'profile': profile, 'departments': departments, 'specializations': specs, 'is_edit': True,
    })


@login_required
def schedule_list(request):
    doctor_filter = request.GET.get('doctor', '')
    schedules = DoctorSchedule.objects.all().select_related('doctor').order_by('-date', 'from_time')
    if doctor_filter:
        schedules = schedules.filter(doctor_id=doctor_filter)
    doctors = DoctorProfile.objects.all().select_related('user')
    return render(request, 'doctors/schedule_list.html', {
        'schedules': schedules, 'doctors': doctors, 'current_doctor': doctor_filter,
    })


@login_required
def schedule_create(request):
    doctors = DoctorProfile.objects.filter(is_available=True).select_related('user')
    if request.method == 'POST':
        DoctorSchedule.objects.create(
            doctor_id=request.POST.get('doctor'),
            date=request.POST.get('date'),
            from_time=request.POST.get('from_time'),
            to_time=request.POST.get('to_time'),
            is_available=request.POST.get('is_available') == 'on',
            reason_unavailable=request.POST.get('reason_unavailable', ''),
        )
        messages.success(request, 'Schedule added')
        return redirect('doctors:schedules')
    return render(request, 'doctors/schedule_form.html', {'doctors': doctors})


@login_required
def schedule_delete(request, pk):
    sched = get_object_or_404(DoctorSchedule, pk=pk)
    if request.method == 'POST':
        sched.delete()
        messages.success(request, 'Schedule deleted')
        return redirect('doctors:schedules')
    return render(request, 'doctors/schedule_confirm_delete.html', {'s': sched})
