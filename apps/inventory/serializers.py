from rest_framework import serializers
from .models import Supplier, SupplyCategory, Supply, PurchaseOrder, PurchaseOrderItem


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyCategory
        fields = '__all__'


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'