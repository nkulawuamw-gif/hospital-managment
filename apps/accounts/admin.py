from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserPermission, Module, RoleModulePermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Activity', {'fields': ('is_online', 'last_activity')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_manage_patients', 'can_manage_billing', 'can_manage_settings']


class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'section', 'order']
    list_filter = ['section']
    search_fields = ['name', 'codename']
    ordering = ['section', 'order']


class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'module_count']
    filter_horizontal = ['modules']

    def module_count(self, obj):
        return obj.modules.count()
    module_count.short_description = 'Modules'


admin.site.register(Module, ModuleAdmin)
admin.site.register(RoleModulePermission, RoleModulePermissionAdmin)
