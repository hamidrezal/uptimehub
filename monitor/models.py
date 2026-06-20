import secrets

from django.db import models
from django.utils import timezone
from account.models import User


class Server(models.Model):
    TYPE_PING = 'ping'
    TYPE_HTTP = 'http'
    TYPE_TCP = 'tcp'
    TYPE_DNS = 'dns'
    TYPE_SSL = 'ssl'
    TYPE_HEARTBEAT = 'heartbeat'
    TYPE_API = 'api'
    TYPE_DOMAIN = 'domain'

    TYPE_CHOICES = [
        (TYPE_HTTP, 'HTTP/HTTPS'),
        (TYPE_PING, '\u067e\u06cc\u0646\u06af'),
        (TYPE_TCP, '\u067e\u0648\u0631\u062a TCP'),
        (TYPE_DNS, 'DNS'),
        (TYPE_SSL, '\u06af\u0648\u0627\u0647\u06cc SSL'),
        (TYPE_HEARTBEAT, 'Cron Job / Heartbeat'),
        (TYPE_API, 'API Endpoint'),
        (TYPE_DOMAIN, '\u0627\u0646\u0642\u0636\u0627\u06cc \u062f\u0627\u0645\u0646\u0647'),
    ]

    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('OPTIONS', 'OPTIONS'),
    ]

    KEYWORD_MODE_CHOICES = [
        ('disabled', '\u0628\u0631\u0631\u0633\u06cc \u0645\u062a\u0646 \u0627\u0646\u062c\u0627\u0645 \u0646\u0634\u0648\u062f'),
        ('contains', '\u067e\u0627\u0633\u062e \u0628\u0627\u06cc\u062f \u0634\u0627\u0645\u0644 \u0645\u062a\u0646 \u0628\u0627\u0634\u062f'),
        ('not_contains', '\u067e\u0627\u0633\u062e \u0646\u0628\u0627\u06cc\u062f \u0634\u0627\u0645\u0644 \u0645\u062a\u0646 \u0628\u0627\u0634\u062f'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servers')
    name = models.CharField(max_length=100, help_text='\u0645\u062b\u0627\u0644: \u0633\u0627\u06cc\u062a \u0627\u0635\u0644\u06cc')
    address = models.CharField(max_length=500, help_text='\u062f\u0627\u0645\u0646\u0647\u060c IP\u060c URL \u06cc\u0627 endpoint')
    monitor_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_HTTP)
    port = models.PositiveIntegerField(blank=True, null=True, help_text='\u0628\u0631\u0627\u06cc TCP/HTTP/SSL')
    is_active = models.BooleanField(default=True)
    check_interval = models.PositiveIntegerField(default=60, help_text='\u062b\u0627\u0646\u06cc\u0647\u061b \u0645\u062b\u0644 30\u060c 60 \u06cc\u0627 300')
    timeout = models.PositiveIntegerField(default=10, help_text='\u062b\u0627\u0646\u06cc\u0647')

    http_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='GET')
    request_headers = models.JSONField(blank=True, null=True, help_text='JSON headers \u0628\u0631\u0627\u06cc API')
    request_body = models.TextField(blank=True, null=True, help_text='Body \u0628\u0631\u0627\u06cc POST/PUT/PATCH')
    expected_status_codes = models.CharField(max_length=100, default='200', help_text='\u0645\u062b\u0627\u0644: 200 \u06cc\u0627 200,201,204')
    expected_keyword = models.CharField(max_length=255, blank=True, null=True, help_text='\u0645\u062a\u0646 \u0645\u0648\u0631\u062f \u0628\u0631\u0631\u0633\u06cc \u062f\u0631 \u067e\u0627\u0633\u062e')
    keyword_mode = models.CharField(max_length=20, choices=KEYWORD_MODE_CHOICES, default='disabled')
    max_response_time_ms = models.PositiveIntegerField(blank=True, null=True, help_text='\u062d\u062f\u0627\u06a9\u062b\u0631 \u0632\u0645\u0627\u0646 \u067e\u0627\u0633\u062e \u0642\u0627\u0628\u0644 \u0642\u0628\u0648\u0644 \u0628\u0631 \u062d\u0633\u0628 \u0645\u06cc\u0644\u06cc \u062b\u0627\u0646\u06cc\u0647')

    ssl_expiry_alert_days = models.PositiveIntegerField(default=14, help_text='\u0647\u0634\u062f\u0627\u0631 \u0627\u0646\u0642\u0636\u0627\u06cc SSL \u0686\u0646\u062f \u0631\u0648\u0632 \u0642\u0628\u0644')
    domain_expiry_alert_days = models.PositiveIntegerField(default=30, help_text='\u0647\u0634\u062f\u0627\u0631 \u0627\u0646\u0642\u0636\u0627\u06cc \u062f\u0627\u0645\u0646\u0647 \u0686\u0646\u062f \u0631\u0648\u0632 \u0642\u0628\u0644')
    heartbeat_grace_seconds = models.PositiveIntegerField(default=120, help_text='\u062d\u062f\u0627\u06a9\u062b\u0631 \u0641\u0627\u0635\u0644\u0647 \u0645\u062c\u0627\u0632 \u0627\u0632 \u0622\u062e\u0631\u06cc\u0646 heartbeat')
    heartbeat_token = models.CharField(max_length=64, unique=True, blank=True)
    last_heartbeat_at = models.DateTimeField(blank=True, null=True)

    last_status = models.BooleanField(default=False)
    last_response_time = models.PositiveIntegerField(blank=True, null=True)
    last_error_message = models.TextField(blank=True, null=True)
    last_check_time = models.DateTimeField(blank=True, null=True)
    ssl_expires_at = models.DateTimeField(blank=True, null=True)
    domain_expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='unique_server_name_per_user')]

    def __str__(self):
        return f'{self.name} ({self.get_monitor_type_display()})'

    def save(self, *args, **kwargs):
        if not self.heartbeat_token:
            self.heartbeat_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def mark_heartbeat(self):
        self.last_heartbeat_at = timezone.now()
        self.save(update_fields=['last_heartbeat_at', 'updated_at'])

    def expected_status_code_set(self):
        codes = set()
        for item in (self.expected_status_codes or '').replace(' ', '').split(','):
            if item.isdigit():
                codes.add(int(item))
        return codes or {200}


class ServerLog(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='logs')
    status = models.BooleanField(help_text='True=UP, False=DOWN')
    response_time = models.PositiveIntegerField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['server', 'created_at'])]

    def __str__(self):
        return f"{self.server.name} - {'UP' if self.status else 'DOWN'} at {self.created_at}"
