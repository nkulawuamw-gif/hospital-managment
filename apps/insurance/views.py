from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import InsuranceCompany, PatientInsurance, InsuranceClaim
from .serializers import InsuranceCompanySerializer, PatientInsuranceSerializer, InsuranceClaimSerializer
from apps.patients.models import Patient


class InsuranceCompanyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer


class PatientInsuranceViewSet(viewsets.ModelViewSet):
    queryset = PatientInsurance.objects.all()
    serializer_class = PatientInsuranceSerializer


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer


# ------------------ Template Views ------------------

@login_required
def company_list(request):
    companies = InsuranceCompany.objects.all().order_by('name')
    return render(request, 'insurance/company_list.html', {'companies': companies})


@login_required
def company_create(request):
    if request.method == 'POST':
        InsuranceCompany.objects.create(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            contact_person=request.POST.get('contact_person', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            coverage_percentage=request.POST.get('coverage_percentage', 80),
        )
        messages.success(request, 'Insurance company added')
        return redirect('insurance:company_list')
    return render(request, 'insurance/company_form.html', {'is_edit': False})


@login_required
def company_edit(request, pk):
    company = get_object_or_404(InsuranceCompany, pk=pk)
    if request.method == 'POST':
        company.name = request.POST.get('name')
        company.code = request.POST.get('code')
        company.contact_person = request.POST.get('contact_person', '')
        company.phone = request.POST.get('phone', '')
        company.email = request.POST.get('email', '')
        company.address = request.POST.get('address', '')
        company.coverage_percentage = request.POST.get('coverage_percentage', 80)
        company.save()
        messages.success(request, 'Insurance company updated')
        return redirect('insurance:company_list')
    return render(request, 'insurance/company_form.html', {'company': company, 'is_edit': True})


@login_required
def policy_list(request):
    policies = PatientInsurance.objects.select_related('patient', 'insurance_company').all().order_by('-created_at')
    return render(request, 'insurance/policy_list.html', {'policies': policies})


@login_required
def policy_create(request):
    patients = Patient.objects.all().order_by('first_name')
    companies = InsuranceCompany.objects.filter(is_active=True)
    if request.method == 'POST':
        PatientInsurance.objects.create(
            patient_id=request.POST.get('patient'),
            insurance_company_id=request.POST.get('insurance_company'),
            policy_number=request.POST.get('policy_number'),
            coverage_percentage=request.POST.get('coverage_percentage', 80),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date') or None,
        )
        messages.success(request, 'Insurance policy added')
        return redirect('insurance:policy_list')
    return render(request, 'insurance/policy_form.html', {'patients': patients, 'companies': companies})


@login_required
def claim_list(request):
    status_filter = request.GET.get('status', '')
    claims = InsuranceClaim.objects.select_related('patient', 'insurance_policy__insurance_company').all().order_by('-created_at')
    if status_filter:
        claims = claims.filter(status=status_filter)
    return render(request, 'insurance/claim_list.html', {'claims': claims, 'current_status': status_filter})


@login_required
def claim_create(request):
    patients = Patient.objects.all().order_by('first_name')
    policies = PatientInsurance.objects.filter(is_active=True).select_related('patient', 'insurance_company')
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        policy_id = request.POST.get('insurance_policy')
        claim = InsuranceClaim.objects.create(
            patient_id=patient_id,
            insurance_policy_id=policy_id,
            invoice_id=request.POST.get('invoice') or None,
            claim_number=f'CLM-{InsuranceClaim.objects.count() + 1:05d}',
            amount_claimed=request.POST.get('amount_claimed', 0),
            notes=request.POST.get('notes', ''),
            submitted_by=request.user,
        )
        messages.success(request, f'Claim {claim.claim_number} created')
        return redirect('insurance:claim_list')
    return render(request, 'insurance/claim_form.html', {'patients': patients, 'policies': policies})


@login_required
def claim_detail(request, pk):
    claim = get_object_or_404(InsuranceClaim.objects.select_related(
        'patient', 'insurance_policy__insurance_company', 'invoice', 'submitted_by', 'approved_by'
    ), pk=pk)
    return render(request, 'insurance/claim_detail.html', {'claim': claim})