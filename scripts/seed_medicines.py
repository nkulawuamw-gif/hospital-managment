"""Seed sample medicines in the pharmacy inventory.

Idempotent: re-runs upsert on (name, strength) so existing rows are updated
with the latest price instead of duplicating.
Run: venv\\Scripts\\python.exe scripts\\seed_medicines.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from decimal import Decimal
from apps.pharmacy.models import Medicine, MedicineCategory


SAMPLES = [
    # (name, strength, unit, brand, generic_name, selling_price, category)
    ('Aspirin',  '300 mg',  Medicine.Unit.TABLET,  'Bayer',     'Acetylsalicylic acid', '1000',  'Analgesics'),
    ('Aspirin',  '81 mg',   Medicine.Unit.TABLET,  'Bayer',     'Acetylsalicylic acid', '600',   'Analgesics'),
    ('Paracetamol', '500 mg', Medicine.Unit.TABLET, 'Panadol', 'Acetaminophen',        '300',   'Analgesics'),
    ('Paracetamol', '120 mg/5 ml', Medicine.Unit.SYRUP, 'Calpol', 'Acetaminophen',   '2500',  'Analgesics'),
    ('Ibuprofen', '400 mg', Medicine.Unit.TABLET,  'Brufen',    'Ibuprofen',            '800',   'Analgesics'),
    ('Diclofenac', '50 mg', Medicine.Unit.TABLET,  'Voltaren',  'Diclofenac sodium',    '900',   'Analgesics'),
    ('Amoxicillin', '500 mg', Medicine.Unit.CAPSULE, 'Amoxil', 'Amoxicillin',        '1500',  'Antibiotics'),
    ('Amoxicillin', '250 mg/5 ml', Medicine.Unit.SYRUP, 'Amoxil', 'Amoxicillin',     '3500',  'Antibiotics'),
    ('Ciprofloxacin', '500 mg', Medicine.Unit.TABLET, 'Cipro', 'Ciprofloxacin',      '1800',  'Antibiotics'),
    ('Metronidazole', '400 mg', Medicine.Unit.TABLET, 'Flagyl', 'Metronidazole',    '700',   'Antibiotics'),
    ('Co-trimoxazole', '480 mg', Medicine.Unit.TABLET, 'Bactrim', 'Sulfamethoxazole/Trimethoprim', '500', 'Antibiotics'),
    ('ORS Sachet', '20.5 g', Medicine.Unit.OTHER, 'WHO-ORS', 'Oral Rehydration Salts', '200', 'Rehydration'),
    ('Multivitamin', '',  Medicine.Unit.TABLET,  'Centrum',  'Multivitamins',          '5000', 'Vitamins'),
    ('Vitamin C', '500 mg', Medicine.Unit.TABLET,  'Ascorbic', 'Ascorbic acid',        '400',  'Vitamins'),
    ('Iron + Folic Acid', '', Medicine.Unit.TABLET, 'Fefol', 'Ferrous sulfate + Folic acid', '1200', 'Vitamins'),
    ('Chlorpheniramine', '4 mg', Medicine.Unit.TABLET, 'Piriton', 'Chlorpheniramine', '300', 'Antihistamines'),
    ('Salbutamol', '4 mg', Medicine.Unit.TABLET, 'Ventolin', 'Salbutamol',           '700',  'Respiratory'),
    ('Salbutamol Inhaler', '100 mcg', Medicine.Unit.OTHER, 'Ventolin', 'Salbutamol', '8500', 'Respiratory'),
    ('Metformin', '500 mg', Medicine.Unit.TABLET, 'Glucophage', 'Metformin HCl',     '600',  'Antidiabetics'),
    ('Amlodipine', '5 mg', Medicine.Unit.TABLET, 'Norvasc', 'Amlodipine besylate',   '800',  'Antihypertensives'),
    ('Losartan', '50 mg', Medicine.Unit.TABLET, 'Cozaar', 'Losartan potassium',   '1200',  'Antihypertensives'),
    ('Hydrochlorothiazide', '25 mg', Medicine.Unit.TABLET, 'HCTZ', 'Hydrochlorothiazide', '500', 'Antihypertensives'),
    ('Atorvastatin', '20 mg', Medicine.Unit.TABLET, 'Lipitor', 'Atorvastatin',      '2000', 'Cardiovascular'),
    ('Omeprazole', '20 mg', Medicine.Unit.CAPSULE, 'Losec', 'Omeprazole',          '900',  'Gastro'),
    ('Antacid Suspension', '200 ml', Medicine.Unit.SYRUP, 'Mylanta', 'Aluminium/Magnesium hydroxide', '4500', 'Gastro'),
]


def run():
    created = updated = 0
    for name, strength, unit, brand, generic, price, cat in SAMPLES:
        category, _ = MedicineCategory.objects.get_or_create(
            name=cat, defaults={'description': f'{cat} group'},
        )
        obj, was_created = Medicine.objects.update_or_create(
            name=name, strength=strength,
            defaults={
                'category': category,
                'unit': unit,
                'brand': brand,
                'generic_name': generic,
                'selling_price': Decimal(price),
                'cost_price': Decimal(price) * Decimal('0.6'),
                'is_active': True,
                'requires_prescription': False,
                'reorder_level': 50,
                'packaging': 'box of 30' if unit in (Medicine.Unit.TABLET, Medicine.Unit.CAPSULE) else '',
            },
        )
        if was_created:
            created += 1
        else:
            updated += 1
        print(f"  {'+' if was_created else '~'} {obj} -> MWK {obj.selling_price}")
    print(f"\nDone. {created} created, {updated} updated. Total: {Medicine.objects.filter(is_active=True).count()}")


if __name__ == '__main__':
    run()
