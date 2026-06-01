from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    filterset_fields = ['action', 'model_name', 'user']


@login_required
def log_list(request):
    action_filter = request.GET.get('action', '')
    logs = AuditLog.objects.select_related('user').all().order_by('-timestamp')
    if action_filter:
        logs = logs.filter(action=action_filter)
    return render(request, 'audit/log_list.html', {'logs': logs, 'current_action': action_filter})
