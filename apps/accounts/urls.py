from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # API
    path('login/', views.LoginAPIView.as_view(), name='auth-login'),
    path('', include(router.urls)),

    # Template views
    path('web/login/', views.login_view, name='login'),
    path('web/logout/', views.logout_view, name='logout'),
    path('web/profile/', views.profile_view, name='profile'),
    path('web/users/', views.user_list_view, name='user_list'),
    path('web/users/create/', views.user_create_view, name='user_create'),
    path('web/users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
]
