import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.doctors.models import Department, Specialization
from apps.laboratory.models import LabTestCategory, LabTest
from apps.pharmacy.models import MedicineCategory, Medicine
from apps.inventory.models import SupplyCategory, Supply
from apps.insurance.models import InsuranceCompany
from apps.audit.models import AuditLog

User = get_user_model()


def create_superuser():
    if not User.objects.filter(email='admin@hospital.com').exists():
        User.objects.create_superuser(
            email='admin@hospital.com',
            password='admin123',
            first_name='Super',
            last_name='Admin',
            role=User.Role.SUPER_ADMIN,
        )
        print('Superuser created: admin@hospital.com / admin123')


def create_departments():
    departments = [
        'Cardiology', 'Pediatrics', 'Orthopedics', 'Neurology',
        'Oncology', 'Radiology', 'Dermatology', 'Emergency Medicine',
        'Obstetrics & Gynecology', 'Ophthalmology', 'ENT', 'Psychiatry',
    ]
    for name in departments:
        Department.objects.get_or_create(name=name)
    print(f'{len(departments)} departments created')


def create_specializations():
    specializations = [
        'General Medicine', 'Cardiology', 'Pediatrics', 'Orthopedic Surgery',
        'Neurology', 'Dermatology', 'Ophthalmology', 'ENT Specialist',
        'Gynecology', 'Psychiatry', 'Radiology', 'Anesthesiology',
    ]
    for name in specializations:
        Specialization.objects.get_or_create(name=name)
    print(f'{len(specializations)} specializations created')


def create_lab_categories():
    categories = ['Blood Tests', 'Urine Tests', 'Imaging', 'Microbiology', 'Pathology']
    for name in categories:
        LabTestCategory.objects.get_or_create(name=name)
    print(f'{len(categories)} lab categories created')


def create_lab_tests():
    tests = [
        ('Complete Blood Count', 'Blood Tests'),
        ('Blood Sugar', 'Blood Tests'),
        ('Lipid Profile', 'Blood Tests'),
        ('Urinalysis', 'Urine Tests'),
        ('X-Ray', 'Imaging'),
        ('CT Scan', 'Imaging'),
        ('MRI', 'Imaging'),
        ('Malaria Test', 'Microbiology'),
        ('HIV Test', 'Microbiology'),
        ('Typhoid Test', 'Microbiology'),
    ]
    for name, cat_name in tests:
        cat = LabTestCategory.objects.filter(name=cat_name).first()
        LabTest.objects.get_or_create(name=name, category=cat)
    print(f'{len(tests)} lab tests created')


def create_medicine_categories():
    categories = ['Antibiotics', 'Pain Relief', 'Cardiovascular', 'Respiratory',
                  'Gastrointestinal', 'Neurological', 'Vitamins', 'Antimalarial']
    for name in categories:
        MedicineCategory.objects.get_or_create(name=name)
    print(f'{len(categories)} medicine categories created')


def create_medicines():
    medicines = [
        ('Amoxicillin', 'Antibiotics', 'Capsule', '500mg'),
        ('Paracetamol', 'Pain Relief', 'Tablet', '500mg'),
        ('Ibuprofen', 'Pain Relief', 'Tablet', '400mg'),
        ('Metformin', 'Cardiovascular', 'Tablet', '500mg'),
        ('Omeprazole', 'Gastrointestinal', 'Capsule', '20mg'),
    ]
    for name, cat_name, unit, strength in medicines:
        cat = MedicineCategory.objects.filter(name=cat_name).first()
        Medicine.objects.get_or_create(
            name=name, category=cat,
            defaults={'unit': unit.lower(), 'strength': strength, 'selling_price': 10, 'cost_price': 5}
        )
    print(f'{len(medicines)} medicines created')


def create_insurance_companies():
    companies = [
        ('AAR Insurance', 'AAR'),
        ('Jubilee Insurance', 'JUB'),
        ('CIC Insurance', 'CIC'),
        ('Britam', 'BRIT'),
        ('NHIF', 'NHIF'),
    ]
    for name, code in companies:
        InsuranceCompany.objects.get_or_create(name=name, code=code)
    print(f'{len(companies)} insurance companies created')


def run():
    create_superuser()
    create_departments()
    create_specializations()
    create_lab_categories()
    create_lab_tests()
    create_medicine_categories()
    create_medicines()
    create_insurance_companies()
    print('Seed data loaded successfully!')


if __name__ == '__main__':
    run()
