from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for msg in messages:
                        errors.append({'field': field, 'message': str(msg)})
                else:
                    errors.append({'field': field, 'message': str(messages)})
        elif isinstance(response.data, list):
            for msg in response.data:
                errors.append({'message': str(msg)})
        response.data = {'errors': errors}
    return response


def generate_patient_id(prefix='PAT'):
    from apps.patients.models import Patient
    import random
    import string
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        pid = f'{prefix}{code}'
        if not Patient.objects.filter(patient_id=pid).exists():
            return pid


def generate_invoice_number(prefix='INV'):
    from apps.billing.models import Invoice
    import random
    import string
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        inv = f'{prefix}{code}'
        if not Invoice.objects.filter(invoice_number=inv).exists():
            return inv
