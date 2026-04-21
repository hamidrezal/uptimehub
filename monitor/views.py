from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from datetime import datetime

from .models import Server
from .utils import check_server
from .forms import ServerForm


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'monitor/dashboard.html'


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerStatusAPIView(View):

    def get(self, request, *args, **kwargs):
        servers = Server.objects.filter(user=request.user, is_active=True)
        results = []

        for server in servers:
            result = check_server(server)
            results.append(result)

        results.sort(key=lambda x: x['status'])

        return JsonResponse({
            'success': True,
            'servers': results,
            'total': len(results),
            'timestamp': datetime.now().isoformat(),
        })


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerListView(ListView):
    model = Server
    template_name = 'monitor/server_list.html'
    context_object_name = 'servers'

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerCreateView(CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'monitor/server_form.html'
    success_url = reverse_lazy('monitor:server_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'سرور با موفقیت اضافه شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'خطا در افزودن سرور. لطفا دوباره تلاش کنید')
        return super().form_invalid(form)


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerUpdateView(UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'monitor/server_form.html'
    success_url = reverse_lazy('monitor:server_list')

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'سرور با موفقیت ویرایش شد')
        return super().form_valid(form)


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerDeleteView(DeleteView):
    model = Server
    template_name = 'monitor/server_confirm_delete.html'
    success_url = reverse_lazy('monitor:server_list')

    def get_queryset(self):
        return Server.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'سرور با موفقیت حذف شد')
        return super().delete(request, *args, **kwargs)


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerCheckView(View):

    def post(self, request, pk, *args, **kwargs):
        server = get_object_or_404(Server, pk=pk, user=request.user)
        result = check_server(server)

        return JsonResponse({
            'success': True,
            'server': result,
        })


# @method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
class ServerToggleView(View):

    def post(self, request, pk, *args, **kwargs):
        server = get_object_or_404(Server, pk=pk, user=request.user)
        server.is_active = not server.is_active
        server.save()

        status_text = 'فعال' if server.is_active else 'غیرفعال'
        messages.success(request, f'سرور {server.name} {status_text} شد')

        return JsonResponse({
            'success': True,
            'is_active': server.is_active,
        })