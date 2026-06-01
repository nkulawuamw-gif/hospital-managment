from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.NotificationViewSet)

urlpatterns = [
    # Template views
    path('web/', views.notification_list, name='list'),
    path('web/<int:pk>/read/', views.mark_read, name='mark_read'),
    path('web/read-all/', views.mark_all_read, name='mark_all_read'),
    path('web/emails/', views.email_log_list, name='email_log_list'),
    path('web/sms/', views.sms_log_list, name='sms_log_list'),

    # API
    path('', include(router.urls)),
]
