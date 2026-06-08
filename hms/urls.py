from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('doctors/', include(('apps.doctors.urls', 'doctors'), namespace='doctors')),
    path('patients/', include(('apps.patients.urls', 'patients'), namespace='patients')),
    path('appointments/', include(('apps.appointments.urls', 'appointments'), namespace='appointments')),
    path('emr/', include(('apps.emr.urls', 'emr'), namespace='emr')),
    path('pharmacy/', include(('apps.pharmacy.urls', 'pharmacy'), namespace='pharmacy')),
    path('laboratory/', include(('apps.laboratory.urls', 'laboratory'), namespace='laboratory')),
    path('billing/', include(('apps.billing.urls', 'billing'), namespace='billing')),
    path('inpatient/', include(('apps.inpatient.urls', 'inpatient'), namespace='inpatient')),
    path('inventory/', include(('apps.inventory.urls', 'inventory'), namespace='inventory')),
    path('insurance/', include(('apps.insurance.urls', 'insurance'), namespace='insurance')),
    path('hr/', include(('apps.hr.urls', 'hr'), namespace='hr')),
    path('reports/', include(('apps.reports.urls', 'reports'), namespace='reports')),
    path('notifications/', include(('apps.notifications.urls', 'notifications'), namespace='notifications')),
    path('audit/', include(('apps.audit.urls', 'audit'), namespace='audit')),
    path('requisitions/', include(('apps.requisitions.urls', 'requisitions'), namespace='requisitions')),
    path('encounters/', include(('apps.encounters.urls', 'encounters'), namespace='encounters')),
    path('', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
