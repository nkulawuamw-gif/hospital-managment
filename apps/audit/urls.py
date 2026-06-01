from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AuditLogViewSet)

urlpatterns = [
    # Template views
    path('web/', views.log_list, name='list'),

    # API
    path('', include(router.urls)),
]
