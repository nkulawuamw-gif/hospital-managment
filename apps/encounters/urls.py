from django.urls import path
from . import views

app_name = 'encounters'

urlpatterns = [
    path('web/active/', views.active_visits, name='active_visits'),
    path('web/completed/', views.completed_visits, name='completed_visits'),
    path('web/start/<int:patient_id>/', views.start_visit, name='start_visit'),
    path('web/queue/', views.department_queue, name='department_queue'),
    path('web/<int:pk>/', views.encounter_detail, name='encounter_detail'),
    path('web/<int:pk>/start/', views.start_encounter, name='start_encounter'),
    path('web/<int:pk>/complete/', views.complete_encounter, name='complete_encounter'),
    path('web/cashier/', views.cashier_list, name='cashier_list'),
    path('web/cashier/<int:pk>/', views.cashier_detail, name='cashier_detail'),
    path('web/cashier/<int:pk>/billed/', views.mark_billed, name='mark_billed'),
]
