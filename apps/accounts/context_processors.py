from django.conf import settings


def site_settings(request):
    return {
        'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'HMS Hospital',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }
