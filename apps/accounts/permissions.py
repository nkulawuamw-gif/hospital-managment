from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.roles


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('super_admin', 'hospital_admin')


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'receptionist'


class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'pharmacist'


class IsLabTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'lab_technician'


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'cashier'


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'accountant'


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'nurse'


class HasModulePermission(BasePermission):
    module_map = {
        'patients': 'can_manage_patients',
        'appointments': 'can_manage_appointments',
        'billing': 'can_manage_billing',
        'pharmacy': 'can_manage_pharmacy',
        'lab': 'can_manage_lab',
        'inventory': 'can_manage_inventory',
        'hr': 'can_manage_hr',
        'reports': 'can_view_reports',
        'settings': 'can_manage_settings',
    }

    def __init__(self, module):
        self.module = module
        super().__init__()

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'super_admin':
            return True
        perm_field = self.module_map.get(self.module)
        if not perm_field:
            return False
        try:
            perm = request.user.custom_permissions
            return getattr(perm, perm_field, False)
        except:
            return False
