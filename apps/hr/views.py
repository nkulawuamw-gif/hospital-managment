from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import Employee, Attendance, Leave
from .serializers import EmployeeSerializer, AttendanceSerializer, LeaveSerializer
from apps.accounts.models import User


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer


# ------------------ Template Views ------------------

@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user').all().order_by('employee_id')
    return render(request, 'hr/employee_list.html', {'employees': employees})


@login_required
def employee_create(request):
    users = User.objects.filter(is_active=True).exclude(employee_profile__isnull=False).order_by('email')
    if request.method == 'POST':
        user_id = request.POST.get('user')
        Employee.objects.create(
            user_id=user_id,
            employee_id=request.POST.get('employee_id'),
            employment_type=request.POST.get('employment_type', 'full_time'),
            date_joined=request.POST.get('date_joined'),
            salary=request.POST.get('salary', 0),
            emergency_contact=request.POST.get('emergency_contact', ''),
            emergency_phone=request.POST.get('emergency_phone', ''),
        )
        messages.success(request, 'Employee added')
        return redirect('hr:employee_list')
    return render(request, 'hr/employee_form.html', {'users': users})


@login_required
def attendance_list(request):
    date_filter = request.GET.get('date', '')
    attendances = Attendance.objects.select_related('employee__user').all().order_by('-date', 'employee__employee_id')
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    return render(request, 'hr/attendance_list.html', {'attendances': attendances, 'current_date': date_filter})


@login_required
def leave_list(request):
    status_filter = request.GET.get('status', '')
    leaves = Leave.objects.select_related('employee__user', 'approved_by').all().order_by('-created_at')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    return render(request, 'hr/leave_list.html', {'leaves': leaves, 'current_status': status_filter})


@login_required
def leave_create(request):
    employees = Employee.objects.select_related('user').filter(is_active=True).order_by('employee_id')
    if request.method == 'POST':
        Leave.objects.create(
            employee_id=request.POST.get('employee'),
            leave_type=request.POST.get('leave_type'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason', ''),
        )
        messages.success(request, 'Leave request submitted')
        return redirect('hr:leave_list')
    return render(request, 'hr/leave_form.html', {'employees': employees})


@login_required
def leave_detail(request, pk):
    leave = get_object_or_404(Leave.objects.select_related('employee__user', 'approved_by'), pk=pk)
    return render(request, 'hr/leave_detail.html', {'leave': leave})