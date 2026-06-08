from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'specializations', views.SpecializationViewSet)
router.register(r'profiles', views.DoctorProfileViewSet)
router.register(r'schedules', views.DoctorScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Departments
    path('web/departments/', views.department_list, name='departments'),
    path('web/departments/create/', views.department_create, name='department_create'),
    path('web/departments/<int:pk>/edit/', views.department_edit, name='department_edit'),

    # Specializations
    path('web/specializations/', views.specialization_list, name='specializations'),

    # Doctors
    path('web/doctors/', views.doctor_list, name='doctors'),
    path('web/doctors/create/', views.doctor_create, name='doctor_create'),
    path('web/doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('web/doctors/<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),

    # Schedules
    path('web/schedules/', views.schedule_list, name='schedules'),
    path('web/schedules/create/', views.schedule_create, name='schedule_create'),
    path('web/schedules/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
]
