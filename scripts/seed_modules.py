import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from apps.accounts.models import Module, RoleModulePermission, User


MODULES = [
    # (name, codename, icon, url_name, section, order)
    ('Dashboard', 'dashboard', 'bi bi-grid-1x2-fill', 'dashboard:dashboard', 'Main', 1),
    ('Patients', 'patients', 'bi bi-people-fill', 'patients:list', 'Patient Care', 1),
    ('Appointments', 'appointments', 'bi bi-calendar-check-fill', 'appointments:list', 'Patient Care', 2),
    ('EMR', 'emr', 'bi bi-file-medical-fill', 'emr:list', 'Patient Care', 3),
    ('Pharmacy', 'pharmacy', 'bi bi-capsule-fill', 'pharmacy:medicines', 'Services', 1),
    ('Laboratory', 'laboratory', 'bi bi-flask-fill', 'laboratory:request_list', 'Services', 2),
    ('Billing', 'billing', 'bi bi-currency-dollar', 'billing:invoice_list', 'Finance', 1),
    ('Insurance', 'insurance', 'bi bi-shield-fill-check', 'insurance:company_list', 'Finance', 2),
    ('Users', 'users', 'bi bi-person-badge-fill', 'accounts:user_list', 'Administration', 1),
    ('Inventory', 'inventory', 'bi bi-box-seam-fill', 'inventory:supply_list', 'Administration', 2),
    ('HR', 'hr', 'bi bi-person-lines-fill', 'hr:employee_list', 'Administration', 3),
    ('Reports', 'reports', 'bi bi-bar-chart-fill', 'reports:dashboard', 'Administration', 4),
    ('Notifications', 'notifications', 'bi bi-bell-fill', 'notifications:list', 'System', 1),
    ('Audit Log', 'audit', 'bi bi-journal-text', 'audit:list', 'System', 2),
    ('Admin', 'admin', 'bi bi-shield-lock-fill', 'admin:index', 'System', 3),
    ('Landing Settings', 'landing_settings', 'bi bi-layout-three-columns', 'dashboard:landing_settings', 'Administration', 5),
]

ROLE_MODULES = {
    'super_admin': [m[1] for m in MODULES],
    'hospital_admin': [m[1] for m in MODULES],
    'doctor': ['dashboard', 'patients', 'appointments', 'emr', 'pharmacy', 'laboratory'],
    'nurse': ['dashboard', 'patients', 'appointments', 'emr'],
    'receptionist': ['dashboard', 'patients', 'appointments'],
    'pharmacist': ['dashboard', 'pharmacy'],
    'lab_technician': ['dashboard', 'laboratory'],
    'cashier': ['dashboard', 'billing', 'insurance'],
    'accountant': ['dashboard', 'billing', 'insurance', 'reports'],
    'patient': [],
}


def seed():
    for name, codename, icon, url_name, section, order in MODULES:
        Module.objects.get_or_create(
            codename=codename,
            defaults={
                'name': name,
                'icon': icon,
                'url_name': url_name,
                'section': section,
                'order': order,
            }
        )

    module_map = {m.codename: m for m in Module.objects.all()}

    for role_value, codenames in ROLE_MODULES.items():
        perm, _ = RoleModulePermission.objects.get_or_create(role=role_value)
        perm.modules.set([module_map[c] for c in codenames if c in module_map])

    print(f'Seeded {Module.objects.count()} modules and {RoleModulePermission.objects.count()} role permissions')


if __name__ == '__main__':
    seed()
