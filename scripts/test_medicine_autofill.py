"""End-to-end test for the medicine auto-fill on invoice form."""
import os
import sys
import re
import json
import django
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

BASE = 'http://127.0.0.1:8765'
s = requests.Session()

# Login
r = s.get(f'{BASE}/accounts/web/login/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
r = s.post(f'{BASE}/accounts/web/login/', data={
    'csrfmiddlewaretoken': csrf,
    'email': 'admin@hospital.com',
    'password': 'admin123',
}, headers={'Referer': f'{BASE}/accounts/web/login/'}, allow_redirects=False)
print(f'Login: {r.status_code} -> {r.headers.get("Location")}')

# Load create page
r = s.get(f'{BASE}/billing/web/create/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
print(f'Create page: {r.status_code}, {len(r.text)} bytes')
print(f'  has datalist: {"id=\"medicinesList\"" in r.text}')
print(f'  has treatment-input: {"treatment-input" in r.text}')
print(f'  has medicine_id: {"name=\"medicine_id" in r.text}')
print(f'  has Aspirin option: {"Aspirin (300 mg)" in r.text}')

# Get a patient
from apps.patients.models import Patient
patient_pk = Patient.objects.filter(is_active=True).first().pk
print(f'Patient pk: {patient_pk}')

# POST invoice with 3 rows
r = s.post(f'{BASE}/billing/web/create/', data={
    'csrfmiddlewaretoken': csrf,
    'patient': patient_pk,
    'due_date': '2026-07-15',
    'discount': '0',
    'description[]': ['Aspirin (300 mg)', 'Paracetamol (500 mg)', 'Surgery consultation fee'],
    'quantity[]': ['2', '5', '1'],
    'unit_price[]': ['1000', '300', '15000'],
    'medicine_id[]': ['1', '3', ''],
    'notes': 'End-to-end test of medicine auto-fill',
}, headers={'Referer': f'{BASE}/billing/web/create/'}, allow_redirects=False)
print(f'\nPOST: {r.status_code} -> {r.headers.get("Location")}')

# Verify
from apps.billing.models import Invoice
inv = Invoice.objects.order_by('-pk').first()
print(f'\nLatest invoice: {inv.invoice_number}')
print(f'  subtotal={inv.subtotal} total={inv.total}')
for item in inv.items.all():
    med = item.medicine
    label = f'  {item.description!r} x{item.quantity} @ MWK {item.unit_price} = MWK {item.total_price}'
    label += f'  medicine_id={med.id if med else None} name={med.name if med else None}'
    print(label)

# Test the API
r = s.get(f'{BASE}/billing/api/medicines/?q=para')
print(f'\nAPI /medicines/?q=para: {r.status_code}')
data = r.json()
print(f'  count={data["count"]}')
for m in data['results'][:5]:
    print(f'  {m["label"]} - MWK {m["selling_price"]}')
