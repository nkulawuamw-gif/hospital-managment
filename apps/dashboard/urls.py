from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('book-appointment/', views.book_appointment_view, name='book_appointment'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
