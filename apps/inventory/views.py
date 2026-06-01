from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import Supplier, SupplyCategory, Supply, PurchaseOrder, PurchaseOrderItem, StockReceiving, StockIssue, StockIssueItem
from .serializers import SupplierSerializer, SupplyCategorySerializer, SupplySerializer, PurchaseOrderSerializer


# ------------------ API Views ------------------

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplyCategoryViewSet(viewsets.ModelViewSet):
    queryset = SupplyCategory.objects.all()
    serializer_class = SupplyCategorySerializer


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# ------------------ Template Views ------------------

@login_required
def supply_list(request):
    category_filter = request.GET.get('category', '')
    supplies = Supply.objects.all().order_by('name')
    if category_filter:
        supplies = supplies.filter(category_id=category_filter)
    categories = SupplyCategory.objects.all()
    return render(request, 'inventory/supply_list.html', {
        'supplies': supplies, 'categories': categories, 'current_category': category_filter,
    })


@login_required
def supply_create(request):
    categories = SupplyCategory.objects.all()
    if request.method == 'POST':
        Supply.objects.create(
            name=request.POST.get('name'),
            category_id=request.POST.get('category') or None,
            unit=request.POST.get('unit', 'piece'),
            reorder_level=request.POST.get('reorder_level', 10),
            current_stock=request.POST.get('current_stock', 0),
            unit_price=request.POST.get('unit_price', 0),
        )
        messages.success(request, 'Supply item added')
        return redirect('inventory:supply_list')
    return render(request, 'inventory/supply_form.html', {'categories': categories, 'is_edit': False})


@login_required
def supply_edit(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    categories = SupplyCategory.objects.all()
    if request.method == 'POST':
        supply.name = request.POST.get('name')
        supply.category_id = request.POST.get('category') or None
        supply.unit = request.POST.get('unit')
        supply.reorder_level = request.POST.get('reorder_level', 10)
        supply.current_stock = request.POST.get('current_stock', 0)
        supply.unit_price = request.POST.get('unit_price', 0)
        supply.save()
        messages.success(request, 'Supply item updated')
        return redirect('inventory:supply_list')
    return render(request, 'inventory/supply_form.html', {'supply': supply, 'categories': categories, 'is_edit': True})


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_create(request):
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name'),
            contact_person=request.POST.get('contact_person', ''),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
        )
        messages.success(request, 'Supplier added')
        return redirect('inventory:supplier_list')
    return render(request, 'inventory/supplier_form.html')


@login_required
def po_list(request):
    status_filter = request.GET.get('status', '')
    pos = PurchaseOrder.objects.all().order_by('-created_at')
    if status_filter:
        pos = pos.filter(status=status_filter)
    return render(request, 'inventory/po_list.html', {'pos': pos, 'current_status': status_filter})


@login_required
def po_create(request):
    suppliers = Supplier.objects.filter(is_active=True)
    supplies = Supply.objects.filter(is_active=True)
    if request.method == 'POST':
        po = PurchaseOrder.objects.create(
            supplier_id=request.POST.get('supplier'),
            order_number=f'PO-{PurchaseOrder.objects.count() + 1:05d}',
            notes=request.POST.get('notes', ''),
            ordered_by=request.user,
        )
        supply_ids = request.POST.getlist('supply[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('unit_price[]')
        total = Decimal('0.00')
        for i in range(len(supply_ids)):
            if supply_ids[i] and quantities[i] and prices[i]:
                qty = int(quantities[i])
                price = Decimal(prices[i])
                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    supply_id=supply_ids[i],
                    quantity_ordered=qty,
                    unit_price=price,
                    total_price=qty * price,
                )
                total += qty * price
        po.total_amount = total
        po.save()
        messages.success(request, f'Purchase Order {po.order_number} created')
        return redirect('inventory:po_list')
    return render(request, 'inventory/po_form.html', {'suppliers': suppliers, 'supplies': supplies})


@login_required
def po_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'inventory/po_detail.html', {'po': po})


@login_required
def receive_stock(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        receiving = StockReceiving.objects.create(
            purchase_order=po,
            received_by=request.user,
            notes=request.POST.get('notes', ''),
        )
        for item in po.items.all():
            qty = int(request.POST.get(f'qty_{item.pk}', item.quantity_ordered))
            item.quantity_received = qty
            item.save()
            item.supply.current_stock += qty
            item.supply.save()
        po.status = PurchaseOrder.Status.RECEIVED
        po.save()
        messages.success(request, 'Stock received')
        return redirect('inventory:po_detail', pk=pk)
    return render(request, 'inventory/receive_stock.html', {'po': po})


@login_required
def stock_issue(request):
    supplies = Supply.objects.filter(is_active=True)
    if request.method == 'POST':
        issue = StockIssue.objects.create(
            issued_to=request.POST.get('issued_to'),
            issued_by=request.user,
            notes=request.POST.get('notes', ''),
        )
        supply_ids = request.POST.getlist('supply[]')
        quantities = request.POST.getlist('quantity[]')
        for i in range(len(supply_ids)):
            if supply_ids[i] and quantities[i]:
                qty = int(quantities[i])
                supply = Supply.objects.get(pk=supply_ids[i])
                if supply.current_stock >= qty:
                    StockIssueItem.objects.create(
                        stock_issue=issue, supply=supply, quantity=qty
                    )
                    supply.current_stock -= qty
                    supply.save()
        messages.success(request, 'Stock issued')
        return redirect('inventory:supply_list')
    return render(request, 'inventory/stock_issue.html', {'supplies': supplies})


@login_required
def issue_history(request):
    issues = StockIssue.objects.all().order_by('-issued_at')
    return render(request, 'inventory/issue_history.html', {'issues': issues})
