from django.urls import path
from . import views
from .admin_views import landing_settings_view

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('book-appointment/', views.book_appointment_view, name='book_appointment'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('landing-settings/', landing_settings_view, name='landing_settings'),
    path('settings/', views.settings_view, name='settings'),
]
