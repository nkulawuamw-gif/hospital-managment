from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_report, name='report-generate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
