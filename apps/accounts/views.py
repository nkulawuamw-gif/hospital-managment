from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, UserPermission
from .serializers import UserSerializer, UserCreateSerializer, ChangePasswordSerializer, UserPermissionSerializer


# ------------------ API Views ------------------

class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.data['old_password']):
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response({'message': 'Password changed'})


# ------------------ Template Views ------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_role_dashboard_url(request.user.role))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}')
            return redirect(get_role_dashboard_url(user.role))
        messages.error(request, 'Invalid email or password')
    return render(request, 'registration/login.html')


def get_role_dashboard_url(role):
    role_urls = {
        'super_admin': 'dashboard:dashboard',
        'hospital_admin': 'dashboard:dashboard',
        'doctor': 'dashboard:dashboard',
        'nurse': 'dashboard:dashboard',
        'receptionist': 'dashboard:dashboard',
        'pharmacist': 'dashboard:dashboard',
        'lab_technician': 'dashboard:dashboard',
        'cashier': 'dashboard:dashboard',
        'accountant': 'dashboard:dashboard',
        'patient': 'dashboard:dashboard',
    }
    return role_urls.get(role, 'dashboard:dashboard')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_create_view(request):
    roles = User.Role.choices
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(
                email=email, password=password,
                first_name=first_name, last_name=last_name,
                role=role
            )
            messages.success(request, f'User {user.email} created successfully')
            return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'roles': roles, 'is_edit': False})


@login_required
def user_edit_view(request, pk):
    user = User.objects.get(pk=pk)
    roles = User.Role.choices
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.role = request.POST.get('role')
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        messages.success(request, 'User updated')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'edit_user': user, 'roles': roles, 'is_edit': True})
