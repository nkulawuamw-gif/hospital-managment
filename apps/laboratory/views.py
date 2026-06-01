from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import LabTestCategory, LabTest, LabTestParameter, LabRequest, LabRequestItem, LabResultParameter
from .serializers import LabTestCategorySerializer, LabTestSerializer, LabTestParameterSerializer, LabRequestSerializer, LabRequestItemSerializer, LabResultParameterSerializer
from apps.patients.models import Patient
from apps.accounts.models import User


# ------------------ API Views ------------------

class LabTestCategoryViewSet(viewsets.ModelViewSet):
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer


class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


class LabTestParameterViewSet(viewsets.ModelViewSet):
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer


class LabRequestViewSet(viewsets.ModelViewSet):
    queryset = LabRequest.objects.all()
    serializer_class = LabRequestSerializer


class LabRequestItemViewSet(viewsets.ModelViewSet):
    queryset = LabRequestItem.objects.all()
    serializer_class = LabRequestItemSerializer


class LabResultParameterViewSet(viewsets.ModelViewSet):
    queryset = LabResultParameter.objects.all()
    serializer_class = LabResultParameterSerializer


# ------------------ Template Views ------------------

@login_required
def test_list(request):
    categories = LabTestCategory.objects.all()
    cat_filter = request.GET.get('category', '')
    tests = LabTest.objects.filter(is_active=True).order_by('name')
    if cat_filter:
        tests = tests.filter(category_id=cat_filter)
    return render(request, 'laboratory/test_list.html', {
        'tests': tests, 'categories': categories, 'current_category': cat_filter,
    })


@login_required
def request_list(request):
    status_filter = request.GET.get('status', '')
    requests = LabRequest.objects.all().order_by('-created_at')
    if status_filter:
        requests = requests.filter(status=status_filter)
    return render(request, 'laboratory/request_list.html', {
        'requests': requests, 'current_status': status_filter,
    })


@login_required
def request_create(request):
    patients = Patient.objects.filter(is_active=True)
    doctors = User.objects.filter(role='doctor', is_active=True)
    tests = LabTest.objects.filter(is_active=True)

    if request.method == 'POST':
        lab_request = LabRequest.objects.create(
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            priority=request.POST.get('priority', 'routine'),
            clinical_notes=request.POST.get('clinical_notes', ''),
        )
        test_ids = request.POST.getlist('tests')
        for tid in test_ids:
            LabRequestItem.objects.create(lab_request=lab_request, test_id=tid)
        messages.success(request, 'Lab request created')
        return redirect('laboratory:request_list')

    return render(request, 'laboratory/request_form.html', {
        'patients': patients, 'doctors': doctors, 'tests': tests,
    })


@login_required
def request_detail(request, pk):
    lab_request = get_object_or_404(LabRequest, pk=pk)
    return render(request, 'laboratory/request_detail.html', {'r': lab_request})


@login_required
def collect_sample(request, pk):
    lab_request = get_object_or_404(LabRequest, pk=pk)
    lab_request.status = LabRequest.Status.SAMPLE_COLLECTED
    lab_request.sample_collected_by = request.user
    lab_request.sample_collected_at = datetime.now()
    lab_request.save()
    messages.success(request, 'Sample collected')
    return redirect('laboratory:request_detail', pk=pk)


@login_required
def enter_results(request, pk):
    lab_request = get_object_or_404(LabRequest, pk=pk)
    if request.method == 'POST':
        for item in lab_request.items.all():
            result = request.POST.get(f'result_{item.pk}', '')
            is_abnormal = request.POST.get(f'abnormal_{item.pk}') == 'on'
            item.result = result
            item.is_abnormal = is_abnormal
            item.save()

            for param in item.parameter_results.all():
                val = request.POST.get(f'param_{param.pk}', '')
                abnormal = request.POST.get(f'param_abnormal_{param.pk}') == 'on'
                param.value = val
                param.is_abnormal = abnormal
                param.save()

        lab_request.status = LabRequest.Status.COMPLETED
        lab_request.processed_by = request.user
        lab_request.processed_at = datetime.now()
        lab_request.save()
        messages.success(request, 'Results saved')
        return redirect('laboratory:request_detail', pk=pk)
    return render(request, 'laboratory/results_form.html', {'r': lab_request})


@login_required
def approve_results(request, pk):
    lab_request = get_object_or_404(LabRequest, pk=pk)
    lab_request.status = LabRequest.Status.APPROVED
    lab_request.approved_by = request.user
    lab_request.approved_at = datetime.now()
    lab_request.save()
    messages.success(request, 'Results approved')
    return redirect('laboratory:request_detail', pk=pk)
