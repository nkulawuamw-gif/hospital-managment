from django.conf import settings
from .models import RoleModulePermission


def site_settings(request):
    ctx = {
        'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'HMS Hospital',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }
    if request.user.is_authenticated:
        try:
            role_perm = RoleModulePermission.objects.prefetch_related('modules').get(role=request.user.role)
            ctx['user_modules'] = list(role_perm.modules.all().order_by('section', 'order'))
        except RoleModulePermission.DoesNotExist:
            ctx['user_modules'] = []
    return ctx
