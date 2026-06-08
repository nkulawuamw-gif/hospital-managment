from datetime import date, datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, F, Q
from rest_framework import viewsets
from .models import MedicineCategory, Medicine, MedicineBatch, Prescription, PrescriptionItem, Dispensation, Sale, SaleItem
from .serializers import MedicineCategorySerializer, MedicineSerializer, MedicineBatchSerializer, PrescriptionSerializer, PrescriptionItemSerializer, DispensationSerializer, SaleSerializer
from apps.patients.models import Patient


# ------------------ API Views ------------------

class MedicineCategoryViewSet(viewsets.ModelViewSet):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    search_fields = ['name', 'generic_name', 'brand']


class MedicineBatchViewSet(viewsets.ModelViewSet):
    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer


class DispensationViewSet(viewsets.ModelViewSet):
    queryset = Dispensation.objects.all()
    serializer_class = DispensationSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


# ------------------ Template Views ------------------

@login_required
def medicine_list(request):
    category_filter = request.GET.get('category', '')
    medicines = Medicine.objects.all().order_by('name')
    if category_filter:
        medicines = medicines.filter(category_id=category_filter)
    categories = MedicineCategory.objects.all()
    low_stock_count = MedicineBatch.objects.filter(quantity_remaining__lte=F('medicine__reorder_level')).count()
    expired_count = MedicineBatch.objects.filter(expiry_date__lt=date.today()).count()
    return render(request, 'pharmacy/medicine_list.html', {
        'medicines': medicines,
        'categories': categories,
        'current_category': category_filter,
        'low_stock_count': low_stock_count,
        'expired_count': expired_count,
    })


@login_required
def medicine_create(request):
    categories = MedicineCategory.objects.all()
    if request.method == 'POST':
        med = Medicine.objects.create(
            name=request.POST.get('name'),
            category_id=request.POST.get('category') or None,
            brand=request.POST.get('brand', ''),
            generic_name=request.POST.get('generic_name', ''),
            unit=request.POST.get('unit', 'tablet'),
            strength=request.POST.get('strength', ''),
            packaging=request.POST.get('packaging', ''),
            reorder_level=request.POST.get('reorder_level', 10),
            selling_price=request.POST.get('selling_price', 0),
            cost_price=request.POST.get('cost_price', 0),
            requires_prescription=request.POST.get('requires_prescription') == 'on',
        )
        messages.success(request, f'Medicine "{med.name}" added')
        return redirect('pharmacy:medicines')
    return render(request, 'pharmacy/medicine_form.html', {'categories': categories, 'is_edit': False})


@login_required
def medicine_edit(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    categories = MedicineCategory.objects.all()
    if request.method == 'POST':
        med.name = request.POST.get('name')
        med.category_id = request.POST.get('category') or None
        med.brand = request.POST.get('brand', '')
        med.generic_name = request.POST.get('generic_name', '')
        med.unit = request.POST.get('unit')
        med.strength = request.POST.get('strength', '')
        med.packaging = request.POST.get('packaging', '')
        med.reorder_level = request.POST.get('reorder_level', 10)
        med.selling_price = request.POST.get('selling_price', 0)
        med.cost_price = request.POST.get('cost_price', 0)
        med.requires_prescription = request.POST.get('requires_prescription') == 'on'
        med.save()
        messages.success(request, 'Medicine updated')
        return redirect('pharmacy:medicines')
    return render(request, 'pharmacy/medicine_form.html', {'med': med, 'categories': categories, 'is_edit': True})


@login_required
def batch_list(request):
    batches = MedicineBatch.objects.all().order_by('-expiry_date')
    expired = request.GET.get('expired')
    if expired == '1':
        batches = batches.filter(expiry_date__lt=date.today())
    return render(request, 'pharmacy/batch_list.html', {'batches': batches, 'show_expired': expired})


@login_required
def batch_create(request):
    medicines = Medicine.objects.filter(is_active=True)
    if request.method == 'POST':
        MedicineBatch.objects.create(
            medicine_id=request.POST.get('medicine'),
            batch_number=request.POST.get('batch_number'),
            quantity=request.POST.get('quantity', 0),
            quantity_remaining=request.POST.get('quantity', 0),
            expiry_date=request.POST.get('expiry_date'),
            manufacturing_date=request.POST.get('manufacturing_date') or None,
            supplier=request.POST.get('supplier', ''),
        )
        messages.success(request, 'Batch added')
        return redirect('pharmacy:batches')
    return render(request, 'pharmacy/batch_form.html', {'medicines': medicines})


@login_required
def prescription_list(request):
    status_filter = request.GET.get('status', '')
    prescriptions = Prescription.objects.all().order_by('-created_at')
    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)
    return render(request, 'pharmacy/prescription_list.html', {
        'prescriptions': prescriptions,
        'current_status': status_filter,
    })


@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'pharmacy/prescription_detail.html', {'p': prescription})


@login_required
def prescription_dispense(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        Dispensation.objects.create(
            prescription=prescription,
            dispensed_by=request.user,
            notes=request.POST.get('notes', ''),
        )
        for item in prescription.items.all():
            item.is_dispensed = True
            item.quantity_dispensed = item.quantity
            item.save()
        prescription.status = Prescription.Status.DISPENSED
        prescription.save()
        messages.success(request, 'Prescription dispensed')
        return redirect('pharmacy:prescription_detail', pk=pk)
    return render(request, 'pharmacy/dispense.html', {'p': prescription})


# ------------------ Sale POS ------------------

@login_required
def sale_list(request):
    today = date.today()
    date_from = request.GET.get('from', today.replace(day=1).isoformat())
    date_to = request.GET.get('to', today.isoformat())
    sales = Sale.objects.filter(created_at__date__gte=date_from, created_at__date__lte=date_to).select_related('patient', 'sold_by').order_by('-created_at')
    totals = sales.aggregate(total=Sum('total_amount'), count=Count('id'))
    return render(request, 'pharmacy/sale_list.html', {
        'sales': sales,
        'date_from': date_from,
        'date_to': date_to,
        'grand_total': totals['total'] or 0,
        'sale_count': totals['count'] or 0,
    })


@login_required
def sale_create(request):
    patients = Patient.objects.filter(is_active=True).order_by('patient_id')
    medicines = Medicine.objects.filter(is_active=True).order_by('name')
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        if not patient_id:
            messages.error(request, 'Please select a patient')
            return redirect('pharmacy:sale_create')
        medicine_ids = request.POST.getlist('medicine_id')
        quantities = request.POST.getlist('quantity')
        unit_prices = request.POST.getlist('unit_price')
        if not medicine_ids:
            messages.error(request, 'Add at least one medicine')
            return redirect('pharmacy:sale_create')
        sale = Sale.objects.create(
            patient_id=patient_id,
            discount=request.POST.get('discount', 0) or 0,
            payment_method=request.POST.get('payment_method', 'cash'),
            sold_by=request.user,
        )
        grand = Decimal('0')
        for med_id, qty, price in zip(medicine_ids, quantities, unit_prices):
            if not med_id or not qty:
                continue
            qty_i = int(qty)
            if qty_i <= 0:
                continue
            unit_p = Decimal(str(price or 0))
            total_p = unit_p * qty_i
            SaleItem.objects.create(
                sale=sale,
                medicine_id=med_id,
                quantity=qty_i,
                unit_price=unit_p,
                total_price=total_p,
            )
            grand += total_p
        sale.total_amount = grand
        sale.discount = Decimal(str(request.POST.get('discount', 0) or 0))
        sale.save()
        messages.success(request, f'Sale #{sale.id} created. Total: MWK {sale.total_amount - sale.discount:,.0f}')
        return redirect('pharmacy:sale_detail', pk=sale.pk)
    return render(request, 'pharmacy/sale_form.html', {
        'patients': patients,
        'medicines': medicines,
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('patient', 'sold_by').prefetch_related('items__medicine'), pk=pk)
    return render(request, 'pharmacy/sale_detail.html', {'s': sale})


# ------------------ Dispensation history ------------------

@login_required
def dispensation_list(request):
    today = date.today()
    date_from = request.GET.get('from', today.replace(day=1).isoformat())
    date_to = request.GET.get('to', today.isoformat())
    dispensations = Dispensation.objects.filter(
        dispensed_at__date__gte=date_from,
        dispensed_at__date__lte=date_to,
    ).select_related('prescription__patient', 'dispensed_by').order_by('-dispensed_at')
    return render(request, 'pharmacy/dispensation_list.html', {
        'dispensations': dispensations,
        'date_from': date_from,
        'date_to': date_to,
    })
