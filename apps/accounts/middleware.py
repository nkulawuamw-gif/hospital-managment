from django.shortcuts import render
from django.urls import resolve
from .models import RoleModulePermission

NAMESPACE_MODULE_MAP = {
    'dashboard': 'dashboard',
    'patients': 'patients',
    'appointments': 'appointments',
    'emr': 'emr',
    'pharmacy': 'pharmacy',
    'laboratory': 'laboratory',
    'billing': 'billing',
    'insurance': 'insurance',
    'accounts': 'users',
    'inventory': 'inventory',
    'hr': 'hr',
    'reports': 'reports',
    'notifications': 'notifications',
    'audit': 'audit',
    'admin': 'admin',
}

PUBLIC_NAMESPACES = {
    'dashboard',  # landing page, book-appointment
}

PUBLIC_URL_NAMES = {
    'dashboard:home',
    'dashboard:book_appointment',
    'accounts:login',
    'accounts:logout',
    'accounts:profile',
}


class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.user.role in ('super_admin', 'hospital_admin'):
            return self.get_response(request)

        try:
            match = resolve(request.path_info)
        except Exception:
            return self.get_response(request)

        namespace = match.namespace
        url_name = match.url_name or ''
        full_name = f'{namespace}:{url_name}' if namespace else url_name

        if full_name in PUBLIC_URL_NAMES or namespace in PUBLIC_NAMESPACES:
            return self.get_response(request)

        module_codename = NAMESPACE_MODULE_MAP.get(namespace)
        if module_codename is None:
            return self.get_response(request)

        try:
            role_perm = RoleModulePermission.objects.prefetch_related('modules').get(role=request.user.role)
            has_access = role_perm.modules.filter(codename=module_codename).exists()
        except RoleModulePermission.DoesNotExist:
            has_access = False

        if not has_access:
            return render(request, 'accounts/access_denied.html', {
                'module_name': module_codename.title(),
            }, status=403)

        return self.get_response(request)
