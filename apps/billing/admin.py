from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment, Quotation

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'total', 'status', 'due_date']
    list_filter = ['status']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'payment_date']

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    pass