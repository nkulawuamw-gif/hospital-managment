from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('patients/', include('apps.patients.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('doctors/', include('apps.doctors.urls')),
    path('emr/', include('apps.emr.urls')),
    path('inpatient/', include('apps.inpatient.urls')),
    path('pharmacy/', include('apps.pharmacy.urls')),
    path('laboratory/', include('apps.laboratory.urls')),
    path('billing/', include('apps.billing.urls')),
    path('insurance/', include('apps.insurance.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('hr/', include('apps.hr.urls')),
    path('reports/', include('apps.reports.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('audit/', include('apps.audit.urls')),
]
