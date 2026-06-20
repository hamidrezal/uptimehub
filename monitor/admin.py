from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from monitor.models import Server, ServerLog


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'monitor_type', 'address', 'port', 'check_interval',
        'is_active', 'last_status', 'last_response_time', 'last_check_time',
    )
    list_filter = ('monitor_type', 'is_active', 'last_status', 'http_method')
    search_fields = ('name', 'address', 'user__username')
    readonly_fields = (
        'heartbeat_url', 'heartbeat_token', 'last_heartbeat_at', 'last_status',
        'last_response_time', 'last_error_message', 'last_check_time',
        'ssl_expires_at', 'domain_expires_at', 'created_at', 'updated_at',
    )
    fieldsets = (
        ('\u062a\u0646\u0638\u06cc\u0645\u0627\u062a \u0627\u0635\u0644\u06cc', {
            'fields': (
                'user', 'name', 'monitor_type', 'address', 'port', 'is_active',
                'check_interval', 'timeout',
            )
        }),
        ('HTTP / HTTPS \u0648 API Endpoint', {
            'fields': (
                'http_method', 'request_headers', 'request_body',
                'expected_status_codes', 'max_response_time_ms',
                'keyword_mode', 'expected_keyword',
            ),
            'description': '\u0628\u0631\u0627\u06cc \u0645\u0627\u0646\u06cc\u062a\u0648\u0631\u06cc\u0646\u06af HTTP/HTTPS \u0648 API Endpoint \u0628\u0627 Method\u0647\u0627\u06cc GET/POST/PUT/PATCH/DELETE \u0648 \u0628\u0631\u0631\u0633\u06cc Status Code\u060c Response Time \u0648 \u0645\u062a\u0646 \u067e\u0627\u0633\u062e.',
        }),
        ('SSL Certificate', {
            'fields': ('ssl_expiry_alert_days', 'ssl_expires_at'),
            'description': 'SSL expiry alert',
        }),
        ('Domain Expiry', {
            'fields': ('domain_expiry_alert_days', 'domain_expires_at'),
            'description': 'Domain expiry alert',
        }),
        ('Cron Job / Heartbeat', {
            'fields': ('heartbeat_grace_seconds', 'heartbeat_url', 'heartbeat_token', 'last_heartbeat_at'),
        }),
        ('\u0622\u062e\u0631\u06cc\u0646 \u0646\u062a\u06cc\u062c\u0647 \u0645\u0627\u0646\u06cc\u062a\u0648\u0631\u06cc\u0646\u06af', {
            'fields': (
                'last_status', 'last_response_time', 'last_error_message',
                'last_check_time', 'created_at', 'updated_at',
            )
        }),
    )

    @admin.display(description='Heartbeat URL')
    def heartbeat_url(self, obj):
        if not obj.pk or obj.monitor_type != Server.TYPE_HEARTBEAT:
            return '-'
        path = reverse('monitor:heartbeat', args=[obj.heartbeat_token])
        return format_html('<code>{}</code>', path)


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = ('server', 'status', 'response_time', 'error_message', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('server__name', 'error_message')
    readonly_fields = ('server', 'status', 'response_time', 'error_message', 'created_at')
