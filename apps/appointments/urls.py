from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AppointmentViewSet)

urlpatterns = [
    # Template views (must come before API to avoid pk="web" matching)
    path('web/', views.appointment_list, name='list'),
    path('web/create/', views.appointment_create, name='create'),
    path('web/<int:pk>/', views.appointment_detail, name='detail'),
    path('web/<int:pk>/checkin/', views.appointment_checkin, name='checkin'),
    path('web/<int:pk>/checkout/', views.appointment_checkout, name='checkout'),
    path('web/<int:pk>/cancel/', views.appointment_cancel, name='cancel'),
    path('web/calendar/', views.calendar_view, name='calendar'),

    # API
    path('', include(router.urls)),
]
