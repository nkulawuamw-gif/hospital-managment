"""Seed sample wards and doctor departments so the new modules have data to display.

Idempotent: re-runs upsert.
Run: venv\\Scripts\\python.exe scripts\\seed_inpatient_doctors.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from apps.doctors.models import StaffDepartment, Specialization
from apps.inpatient.models import Ward, Bed


STAFF_DEPTS = [
    ('Internal Medicine', 'General medical cases and consultations', 'Block A, 2nd Floor', '+265 1 756 100'),
    ('Surgery', 'General surgery and minor theatre', 'Block B, 1st Floor', '+265 1 756 101'),
    ('Pediatrics', 'Children under 5 and pediatric inpatients', 'Block A, 3rd Floor', '+265 1 756 102'),
    ('Maternity', 'Antenatal, delivery and postnatal care', 'Block C, 1st Floor', '+265 1 756 103'),
    ('Outpatient', 'Walk-in consultations and follow-ups', 'Block A, Ground Floor', '+265 1 756 104'),
    ('Emergency & Casualty', '24/7 emergency care and stabilization', 'Ground Floor, East Wing', '+265 1 756 105'),
    ('Pharmacy', 'Medicine dispensing and counseling', 'Ground Floor, Central', '+265 1 756 106'),
    ('Laboratory', 'Diagnostic testing and sample collection', 'Block B, Ground Floor', '+265 1 756 107'),
]

SPECIALIZATIONS = [
    ('General Practice', 'Primary care for all ages'),
    ('Internal Medicine', 'Adult disease diagnosis and treatment'),
    ('Pediatrics', 'Children and adolescent health'),
    ('Obstetrics & Gynecology', 'Pregnancy, childbirth and female reproductive health'),
    ('General Surgery', 'Surgical procedures'),
    ('Orthopedics', 'Bones, joints and musculoskeletal system'),
    ('Cardiology', 'Heart and cardiovascular system'),
    ('Dermatology', 'Skin, hair and nails'),
    ('ENT', 'Ear, nose and throat'),
    ('Ophthalmology', 'Eye and vision care'),
    ('Dentistry', 'Oral health'),
    ('Anesthesiology', 'Anaesthesia and perioperative care'),
    ('Radiology', 'Medical imaging'),
    ('Pathology', 'Laboratory medicine'),
    ('Emergency Medicine', 'Acute care and trauma'),
    ('Psychiatry', 'Mental health'),
]


WARDS = [
    # (name, type, floor, capacity, charge_per_day, staff_dept)
    ('General Ward A', 'general', '1st Floor', 12, 5000, 'Internal Medicine'),
    ('General Ward B', 'general', '1st Floor', 12, 5000, 'Internal Medicine'),
    ('Pediatric Ward', 'pediatric', '3rd Floor', 10, 6000, 'Pediatrics'),
    ('Maternity Ward', 'maternity', '1st Floor, Block C', 8, 8000, 'Maternity'),
    ('Private Room 1', 'private', '2nd Floor', 1, 25000, 'Internal Medicine'),
    ('Private Room 2', 'private', '2nd Floor', 1, 25000, 'Internal Medicine'),
    ('ICU', 'icu', '1st Floor, East Wing', 4, 50000, 'Emergency & Casualty'),
    ('Emergency Holding', 'emergency', 'Ground Floor', 6, 3000, 'Emergency & Casualty'),
]


def run():
    # Staff departments
    for name, desc, loc, phone in STAFF_DEPTS:
        StaffDepartment.objects.update_or_create(
            name=name,
            defaults={'description': desc, 'location': loc, 'phone': phone, 'is_active': True},
        )
    print(f'Staff departments: {StaffDepartment.objects.count()}')

    # Specializations
    for name, desc in SPECIALIZATIONS:
        Specialization.objects.update_or_create(
            name=name,
            defaults={'description': desc},
        )
    print(f'Specializations: {Specialization.objects.count()}')

    # Wards
    for name, wtype, floor, cap, charge, dept_name in WARDS:
        dept = StaffDepartment.objects.filter(name=dept_name).first()
        ward, created = Ward.objects.update_or_create(
            name=name,
            defaults={
                'type': wtype, 'floor': floor, 'capacity': cap,
                'charge_per_day': charge, 'department': dept, 'is_active': True,
            },
        )
        # Auto-create beds up to capacity
        existing = ward.beds.count()
        for i in range(existing + 1, cap + 1):
            Bed.objects.create(ward=ward, bed_number=f'B{i:02d}')
    print(f'Wards: {Ward.objects.count()} ({Bed.objects.count()} beds total)')


if __name__ == '__main__':
    run()
