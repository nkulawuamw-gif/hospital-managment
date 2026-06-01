from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'leaves', views.LeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('web/employees/', views.employee_list, name='employee_list'),
    path('web/employees/create/', views.employee_create, name='employee_create'),
    path('web/attendance/', views.attendance_list, name='attendance_list'),
    path('web/leaves/', views.leave_list, name='leave_list'),
    path('web/leaves/create/', views.leave_create, name='leave_create'),
    path('web/leaves/<int:pk>/', views.leave_detail, name='leave_detail'),
]