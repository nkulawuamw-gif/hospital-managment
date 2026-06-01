from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class Supplier(models.Model):
    name = models.CharField(max_length=300)
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return self.name


class SupplyCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'supply_categories'

    def __str__(self):
        return self.name


class Supply(models.Model):
    class Unit(models.TextChoices):
        PIECE = 'piece', 'Piece'
        PACK = 'pack', 'Pack'
        BOX = 'box', 'Box'
        LITER = 'liter', 'Liter'
        KILOGRAM = 'kilogram', 'Kilogram'
        METER = 'meter', 'Meter'

    name = models.CharField(max_length=300)
    category = models.ForeignKey(SupplyCategory, on_delete=models.SET_NULL, null=True, related_name='supplies')
    unit = models.CharField(max_length=20, choices=Unit.choices, default=Unit.PIECE)
    reorder_level = models.IntegerField(default=10)
    current_stock = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'supplies'

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        RECEIVED = 'received', 'Received'
        CANCELLED = 'cancelled', 'Cancelled'

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase_orders')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'purchase_orders'

    def __str__(self):
        return f'PO-{self.order_number}'


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='purchase_items')
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchase_order_items'


class StockReceiving(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, related_name='receivings')
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_receivings'


class StockIssue(models.Model):
    issued_to = models.CharField(max_length=200)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_issues')
    notes = models.TextField(blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_issues'


class StockIssueItem(models.Model):
    stock_issue = models.ForeignKey(StockIssue, on_delete=models.CASCADE, related_name='items')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'stock_issue_items'
