from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.InsuranceCompanyViewSet)
router.register(r'policies', views.PatientInsuranceViewSet)
router.register(r'claims', views.InsuranceClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('web/companies/', views.company_list, name='company_list'),
    path('web/companies/create/', views.company_create, name='company_create'),
    path('web/companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('web/policies/', views.policy_list, name='policy_list'),
    path('web/policies/create/', views.policy_create, name='policy_create'),
    path('web/claims/', views.claim_list, name='claim_list'),
    path('web/claims/create/', views.claim_create, name='claim_create'),
    path('web/claims/<int:pk>/', views.claim_detail, name='claim_detail'),
]