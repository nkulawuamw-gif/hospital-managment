from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone

from .models import EncounterMedication, PatientVisit, Encounter


@receiver(pre_save, sender=EncounterMedication)
def set_prices(sender, instance, **kwargs):
    if not instance.pk:
        if not instance.unit_price:
            instance.unit_price = instance.medicine.selling_price
        instance.total_price = instance.unit_price * instance.quantity


@receiver(post_save, sender=EncounterMedication)
def deduct_inventory(sender, instance, created, **kwargs):
    if created:
        from apps.pharmacy.models import MedicineBatch
        qty_to_deduct = instance.quantity
        batches = MedicineBatch.objects.filter(
            medicine=instance.medicine,
            quantity_remaining__gt=0,
            expiry_date__gt=timezone.now().date()
        ).order_by('expiry_date')

        with transaction.atomic():
            for batch in batches:
                if qty_to_deduct <= 0:
                    break
                deduct = min(batch.quantity_remaining, qty_to_deduct)
                batch.quantity_remaining -= deduct
                batch.save()
                qty_to_deduct -= deduct
