from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Notification, EmailLog, SMSLog
from .serializers import NotificationSerializer, EmailLogSerializer, SMSLogSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)


# ------------------ Template Views ------------------

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'notification_list'))


@login_required
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notifications:list')


@login_required
def email_log_list(request):
    logs = EmailLog.objects.all().order_by('-sent_at')
    return render(request, 'notifications/email_log_list.html', {'logs': logs})


@login_required
def sms_log_list(request):
    logs = SMSLog.objects.all().order_by('-sent_at')
    return render(request, 'notifications/sms_log_list.html', {'logs': logs})
