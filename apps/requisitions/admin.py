from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Requisition, RequisitionItem


class RequisitionItemInline(admin.TabularInline):
    model = RequisitionItem
    extra = 1


@admin.register(Requisition)
class RequisitionAdmin(SimpleHistoryAdmin):
    list_display = ['request_number', 'status', 'requested_by', 'department', 'created_at']
    list_filter = ['status', 'department']
    search_fields = ['request_number', 'requested_by__email']
    inlines = [RequisitionItemInline]


@admin.register(RequisitionItem)
class RequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['requisition', 'medicine', 'quantity_requested', 'quantity_delivered']
