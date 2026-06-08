from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from .models import Invoice, InvoiceItem, Payment, Quotation
from .serializers import InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer, QuotationSerializer
from apps.patients.models import Patient
from apps.pharmacy.models import Medicine
from apps.api.utils import generate_invoice_number


# ------------------ API Views ------------------

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer


# ------------------ JSON Helpers ------------------

@require_GET
@login_required
def medicines_api(request):
    """Return active medicines for the invoice/quotation line-item autocomplete.

    Supports ?q=<text> for typeahead filtering; returns the full list if no q is given.
    """
    q = (request.GET.get('q') or '').strip()
    qs = Medicine.objects.filter(is_active=True).order_by('name')
    if q:
        qs = qs.filter(name__icontains=q)
    data = [
        {
            'id': m.id,
            'name': m.name,
            'label': f'{m.name} ({m.strength})'.strip(),
            'strength': m.strength,
            'unit': m.get_unit_display(),
            'selling_price': str(m.selling_price),
        }
        for m in qs[:200]
    ]
    return JsonResponse({'results': data, 'count': qs.count()})


# ------------------ Template Views ------------------

@login_required
def invoice_list(request):
    status_filter = request.GET.get('status', '')
    invoices = Invoice.objects.all().order_by('-created_at')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices, 'current_status': status_filter,
    })


@login_required
def invoice_create(request):
    patients = Patient.objects.filter(is_active=True)
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            patient_id=request.POST.get('patient'),
            invoice_number=generate_invoice_number(),
            due_date=request.POST.get('due_date') or None,
            notes=request.POST.get('notes', ''),
            issued_by=request.user,
        )
        descriptions = request.POST.getlist('description[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('unit_price[]')
        medicine_ids = request.POST.getlist('medicine_id[]')
        subtotal = Decimal('0.00')
        for i in range(len(descriptions)):
            if descriptions[i] and quantities[i] and prices[i]:
                qty = int(quantities[i])
                price = Decimal(prices[i])
                total = qty * price
                med_id = medicine_ids[i] if i < len(medicine_ids) else None
                InvoiceItem.objects.create(
                    invoice=invoice,
                    description=descriptions[i],
                    medicine_id=med_id or None,
                    quantity=qty,
                    unit_price=price,
                    total_price=total,
                )
                subtotal += total
        discount = Decimal(request.POST.get('discount', '0'))
        tax = Decimal(request.POST.get('tax', '0'))
        invoice.subtotal = subtotal
        invoice.discount = discount
        invoice.tax = tax
        invoice.total = subtotal - discount + tax
        invoice.balance = invoice.total
        invoice.save()
        messages.success(request, f'Invoice {invoice.invoice_number} created')
        return redirect('billing:invoice_detail', pk=invoice.pk)
    return render(request, 'billing/invoice_form.html', {
        'patients': patients,
        'medicines': Medicine.objects.filter(is_active=True).order_by('name'),
    })


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/invoice_detail.html', {'inv': invoice})


@login_required
def record_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))
        method = request.POST.get('payment_method', 'cash')
        ref = request.POST.get('transaction_reference', '')
        Payment.objects.create(
            invoice=invoice,
            amount=amount,
            payment_method=method,
            transaction_reference=ref,
            received_by=request.user,
        )
        invoice.amount_paid += amount
        invoice.balance = invoice.total - invoice.amount_paid
        if invoice.balance <= 0:
            invoice.status = Invoice.Status.PAID
        elif invoice.amount_paid > 0:
            invoice.status = Invoice.Status.PARTIAL
        invoice.save()
        messages.success(request, f'Payment of MWK {amount} recorded')
        return redirect('billing:invoice_detail', pk=pk)
    return render(request, 'billing/payment_form.html', {'inv': invoice})


@login_required
def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-created_at')
    return render(request, 'billing/quotation_list.html', {'quotations': quotations})


@login_required
def quotation_create(request):
    patients = Patient.objects.filter(is_active=True)
    if request.method == 'POST':
        items = []
        descs = request.POST.getlist('description[]')
        qties = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('unit_price[]')
        total = Decimal('0.00')
        for i in range(len(descs)):
            if descs[i] and qties[i] and prices[i]:
                qty = int(qties[i])
                price = Decimal(prices[i])
                items.append({'description': descs[i], 'quantity': qty, 'unit_price': str(price), 'total': str(qty * price)})
                total += qty * price
        Quotation.objects.create(
            patient_id=request.POST.get('patient'),
            items=items,
            total_amount=total,
            valid_until=request.POST.get('valid_until'),
            created_by=request.user,
        )
        messages.success(request, 'Quotation created')
        return redirect('billing:quotation_list')
    return render(request, 'billing/quotation_form.html', {
        'patients': patients,
        'medicines': Medicine.objects.filter(is_active=True).order_by('name'),
    })
