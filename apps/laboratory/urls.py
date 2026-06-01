from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.LabTestCategoryViewSet)
router.register(r'tests', views.LabTestViewSet)
router.register(r'parameters', views.LabTestParameterViewSet)
router.register(r'requests', views.LabRequestViewSet)
router.register(r'request-items', views.LabRequestItemViewSet)
router.register(r'result-parameters', views.LabResultParameterViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('web/', views.request_list, name='request_list'),
    path('web/tests/', views.test_list, name='test_list'),
    path('web/create/', views.request_create, name='request_create'),
    path('web/<int:pk>/', views.request_detail, name='request_detail'),
    path('web/<int:pk>/collect/', views.collect_sample, name='collect_sample'),
    path('web/<int:pk>/results/', views.enter_results, name='enter_results'),
    path('web/<int:pk>/approve/', views.approve_results, name='approve_results'),
]
