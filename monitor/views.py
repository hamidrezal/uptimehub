from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import ServerForm
from .models import Server
from .monitoring import ServerMonitor
from .utils import check_server


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'monitor/dashboard.html'
    login_url = 'account:login'


class ServerStatusAPIView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request, *args, **kwargs):
        servers = Server.objects.filter(user=request.user, is_active=True)
        monitor = ServerMonitor(retry_count=2, retry_delay=1)
        results = [monitor.check_with_retry(server) for server in servers]
        results.sort(key=lambda item: item['status'])
        return JsonResponse({'success': True, 'servers': results, 'total': len(results), 'timestamp': timezone.now().isoformat()})


class ServerListView(LoginRequiredMixin, ListView):
    model = Server
    template_name = 'monitor/server_list.html'
    context_object_name = 'servers'
    login_url = 'account:login'

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)


class ServerCreateView(LoginRequiredMixin, CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'monitor/server_form.html'
    success_url = reverse_lazy('monitor:server_list')
    login_url = 'account:login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'مانیتور با موفقیت اضافه شد.')
        return super().form_valid(form)


class ServerUpdateView(LoginRequiredMixin, UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'monitor/server_form.html'
    success_url = reverse_lazy('monitor:server_list')
    login_url = 'account:login'

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'مانیتور با موفقیت ویرایش شد.')
        return super().form_valid(form)


class ServerDeleteView(LoginRequiredMixin, DeleteView):
    model = Server
    template_name = 'monitor/server_confirm_delete.html'
    success_url = reverse_lazy('monitor:server_list')
    login_url = 'account:login'

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'مانیتور با موفقیت حذف شد.')
        return super().form_valid(form)


class ServerCheckView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request, pk, *args, **kwargs):
        server = get_object_or_404(Server, pk=pk, user=request.user)
        return JsonResponse({'success': True, 'server': check_server(server)})


class ServerToggleView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request, pk, *args, **kwargs):
        server = get_object_or_404(Server, pk=pk, user=request.user)
        server.is_active = not server.is_active
        server.save(update_fields=['is_active', 'updated_at'])
        return JsonResponse({'success': True, 'is_active': server.is_active})


class HeartbeatView(View):
    def get(self, request, token, *args, **kwargs):
        return self._mark(token)

    def post(self, request, token, *args, **kwargs):
        return self._mark(token)

    def _mark(self, token):
        server = get_object_or_404(Server, heartbeat_token=token, monitor_type=Server.TYPE_HEARTBEAT, is_active=True)
        server.mark_heartbeat()
        return JsonResponse({'success': True, 'server': server.name, 'received_at': server.last_heartbeat_at.isoformat()})
