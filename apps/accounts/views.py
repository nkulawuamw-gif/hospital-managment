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
    if request.user.role not in ('super_admin', 'hospital_admin'):
        messages.error(request, 'You do not have permission to add users.')
        return redirect('dashboard:dashboard')
    roles = User.Role.choices
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        role = request.POST.get('role') or ''
        password = request.POST.get('password') or ''
        password_confirm = request.POST.get('password_confirm') or ''
        phone = (request.POST.get('phone') or '').strip()

        valid_roles = [r[0] for r in User.Role.choices]
        if not email or not first_name or not last_name:
            messages.error(request, 'First name, last name, and email are required.')
        elif role not in valid_roles:
            messages.error(request, 'Invalid role selected.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, f'A user with email {email} already exists.')
        else:
            is_admin_role = role in ('super_admin', 'hospital_admin')
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                phone=phone,
                is_staff=is_admin_role,
                is_superuser=(role == 'super_admin'),
            )
            messages.success(
                request,
                f'User {user.get_full_name()} ({user.get_role_display()}) created successfully.'
            )
            return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'roles': roles, 'is_edit': False})


@login_required
def user_edit_view(request, pk):
    if request.user.role not in ('super_admin', 'hospital_admin'):
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('dashboard:dashboard')
    user = User.objects.get(pk=pk)
    roles = User.Role.choices
    if request.method == 'POST':
        user.first_name = (request.POST.get('first_name') or '').strip()
        user.last_name = (request.POST.get('last_name') or '').strip()
        new_role = request.POST.get('role') or user.role
        if new_role in [r[0] for r in User.Role.choices]:
            user.role = new_role
        user.phone = (request.POST.get('phone') or '').strip()
        user.is_active = request.POST.get('is_active') == 'on'
        if user.role in ('super_admin', 'hospital_admin'):
            user.is_staff = True
        if user.role == 'super_admin':
            user.is_superuser = True
        new_password = request.POST.get('password') or ''
        if new_password:
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'accounts/user_form.html', {'edit_user': user, 'roles': roles, 'is_edit': True})
            user.set_password(new_password)
        user.save()
        messages.success(request, f'User {user.get_full_name()} updated successfully.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'edit_user': user, 'roles': roles, 'is_edit': True})
