from django.conf import settings
from .models import RoleModulePermission
from apps.dashboard.models import SiteSetting


def site_settings(request):
    ctx = {
        'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'HMS Hospital',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }

    site = SiteSetting.get_settings()
    if site:
        ctx['theme'] = {
            'theme_mode': site.theme_mode,
            'primary_color': site.primary_color,
            'primary_light': site.primary_light,
            'primary_dark': site.primary_dark,
            'accent_color': site.accent_color,
            'sidebar_bg_start': site.sidebar_bg_start,
            'sidebar_bg_end': site.sidebar_bg_end,
            'card_bg': site.card_bg,
            'card_border': site.card_border,
            'body_bg': site.body_bg,
            'text_primary': site.text_primary,
            'text_muted': site.text_muted,
            'topbar_bg': site.topbar_bg,
        }

    if request.user.is_authenticated:
        try:
            role_perm = RoleModulePermission.objects.prefetch_related('modules').get(role=request.user.role)
            ctx['user_modules'] = list(role_perm.modules.all().order_by('section', 'order'))
        except RoleModulePermission.DoesNotExist:
            ctx['user_modules'] = []
    return ctx
