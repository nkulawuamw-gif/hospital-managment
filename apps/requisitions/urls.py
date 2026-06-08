from django.urls import path
from . import views

urlpatterns = [
    path('web/requisitions/', views.requisition_list, name='requisition_list'),
    path('web/requisitions/create/', views.requisition_create, name='requisition_create'),
    path('web/requisitions/<int:pk>/', views.requisition_detail, name='requisition_detail'),
    path('web/requisitions/<int:pk>/approve/', views.requisition_approve, name='requisition_approve'),
    path('web/requisitions/<int:pk>/process/', views.requisition_process, name='requisition_process'),
    path('web/requisitions/<int:pk>/dispatch/', views.requisition_dispatch, name='requisition_dispatch'),
]
