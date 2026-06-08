from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Requisition, RequisitionItem
from apps.pharmacy.models import Medicine
from apps.doctors.models import StaffDepartment
from apps.notifications.models import Notification


def notify(recipient, title, message, link=''):
    Notification.objects.create(
        recipient=recipient,
        type='system',
        title=title,
        message=message,
        link=link,
    )


def generate_request_number():
    last = Requisition.objects.order_by('-id').first()
    if last:
        num = int(last.request_number.split('-')[1]) + 1
    else:
        num = 1
    return f'REQ-{num:04d}'


@login_required
def requisition_list(request):
    user = request.user
    if user.role in ('super_admin', 'hospital_admin'):
        requisitions = Requisition.objects.all()
    elif user.role == 'pharmacist':
        requisitions = Requisition.objects.filter(
            Q(status='approved') | Q(status='processing') | Q(dispatched_by=user)
        )
    else:
        requisitions = Requisition.objects.filter(requested_by=user)

    status_filter = request.GET.get('status')
    if status_filter:
        requisitions = requisitions.filter(status=status_filter)

    return render(request, 'requisitions/requisition_list.html', {
        'requisitions': requisitions,
        'current_status': status_filter,
    })


@login_required
def requisition_create(request):
    medicines = Medicine.objects.filter(is_active=True)
    departments = StaffDepartment.objects.filter(is_active=True)

    if request.method == 'POST':
        department_id = request.POST.get('department')
        notes = request.POST.get('notes', '')
        medicine_ids = request.POST.getlist('medicine[]')
        quantities = request.POST.getlist('quantity[]')

        if not medicine_ids or not any(int(q or 0) > 0 for q in quantities):
            messages.error(request, 'Please add at least one item with quantity > 0.')
            return render(request, 'requisitions/requisition_form.html', {
                'medicines': medicines,
                'departments': departments,
            })

        requisition = Requisition.objects.create(
            request_number=generate_request_number(),
            requested_by=request.user,
            department_id=department_id or None,
            notes=notes,
        )

        for med_id, qty in zip(medicine_ids, quantities):
            qty = int(qty or 0)
            if qty > 0 and med_id:
                RequisitionItem.objects.create(
                    requisition=requisition,
                    medicine_id=med_id,
                    quantity_requested=qty,
                )

        messages.success(request, f'Requisition {requisition.request_number} submitted for approval.')
        return redirect('requisitions:requisition_detail', pk=requisition.pk)

    return render(request, 'requisitions/requisition_form.html', {
        'medicines': medicines,
        'departments': departments,
    })


@login_required
def requisition_detail(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    user = request.user
    can_approve = user.role in ('super_admin', 'hospital_admin') and requisition.status == 'pending'
    can_process = user.role == 'pharmacist' and requisition.status == 'approved'
    can_dispatch = user.role == 'pharmacist' and requisition.status == 'processing'
    return render(request, 'requisitions/requisition_detail.html', {
        'r': requisition,
        'can_approve': can_approve,
        'can_process': can_process,
        'can_dispatch': can_dispatch,
    })


@login_required
def requisition_approve(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if request.user.role not in ('super_admin', 'hospital_admin'):
        messages.error(request, 'You do not have permission to approve requisitions.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if requisition.status != 'pending':
        messages.error(request, 'This requisition has already been reviewed.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        approval_notes = request.POST.get('approval_notes', '')

        if action == 'approve':
            for item in requisition.items.all():
                qty = request.POST.get(f'approved_qty_{item.pk}')
                item.quantity_approved = int(qty or item.quantity_requested)
                item.save()

            requisition.status = Requisition.Status.APPROVED
            requisition.approved_by = request.user
            requisition.approved_at = timezone.now()
            requisition.approval_notes = approval_notes
            requisition.save()

            for u in requisition.requested_by.__class__.objects.filter(role='pharmacist', is_active=True):
                notify(u, 'New Requisition Approved',
                       f'Requisition {requisition.request_number} has been approved and is ready for processing.',
                       f'/requisitions/web/requisitions/{requisition.pk}/')

            notify(requisition.requested_by, 'Requisition Approved',
                   f'Your requisition {requisition.request_number} has been approved.',
                   f'/requisitions/web/requisitions/{requisition.pk}/')

            messages.success(request, f'Requisition {requisition.request_number} approved.')
        elif action == 'reject':
            requisition.status = Requisition.Status.REJECTED
            requisition.approved_by = request.user
            requisition.approved_at = timezone.now()
            requisition.approval_notes = approval_notes
            requisition.save()

            notify(requisition.requested_by, 'Requisition Rejected',
                   f'Your requisition {requisition.request_number} was rejected. Reason: {approval_notes or "Not specified"}',
                   f'/requisitions/web/requisitions/{requisition.pk}/')

            messages.warning(request, f'Requisition {requisition.request_number} rejected.')
        return redirect('requisitions:requisition_detail', pk=pk)

    return render(request, 'requisitions/requisition_approve.html', {
        'r': requisition,
    })


@login_required
def requisition_process(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if request.user.role != 'pharmacist':
        messages.error(request, 'Only pharmacists can process requisitions.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if requisition.status != 'approved':
        messages.error(request, 'This requisition must be approved first.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if request.method == 'POST':
        requisition.status = Requisition.Status.PROCESSING
        requisition.processed_by = request.user
        requisition.processed_at = timezone.now()
        requisition.save()

        notify(requisition.requested_by, 'Requisition Being Processed',
               f'Your requisition {requisition.request_number} is now being processed by pharmacy.',
               f'/requisitions/web/requisitions/{requisition.pk}/')

        messages.success(request, f'Requisition {requisition.request_number} is now being processed.')
        return redirect('requisitions:requisition_detail', pk=pk)

    return redirect('requisitions:requisition_detail', pk=pk)


@login_required
def requisition_dispatch(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if request.user.role != 'pharmacist':
        messages.error(request, 'Only pharmacists can dispatch requisitions.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if requisition.status not in ('approved', 'processing'):
        messages.error(request, 'This requisition cannot be dispatched in its current state.')
        return redirect('requisitions:requisition_detail', pk=pk)

    if request.method == 'POST':
        dispatch_notes = request.POST.get('dispatch_notes', '')
        for item in requisition.items.all():
            qty = request.POST.get(f'delivered_qty_{item.pk}')
            if qty:
                item.quantity_delivered = int(qty)
                item.save()

        requisition.status = Requisition.Status.DISPATCHED
        requisition.dispatched_by = request.user
        requisition.dispatched_at = timezone.now()
        requisition.dispatch_notes = dispatch_notes
        requisition.save()

        notify(requisition.requested_by, 'Requisition Dispatched',
               f'Your requisition {requisition.request_number} has been dispatched by pharmacy.',
               f'/requisitions/web/requisitions/{requisition.pk}/')

        messages.success(request, f'Requisition {requisition.request_number} dispatched with confirmation.')
        return redirect('requisitions:requisition_detail', pk=pk)

    return render(request, 'requisitions/requisition_dispatch.html', {
        'r': requisition,
    })
