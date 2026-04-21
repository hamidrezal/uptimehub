from django.db import models
from account.models import User

class Server(models.Model):
    TYPE_CHOICES = [
        ('ping', 'Ping'),
        ('http', 'HTTP/HTTPS'),
        ('tcp', 'TCP Port'),
        ('dns', 'DNS'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='servers')
    name = models.CharField(max_length=100, help_text="مثال: سرور اصلی من")
    address = models.CharField(max_length=200, help_text="مثال: google.com یا 8.8.8.8")
    monitor_type = models.CharField(max_length=10,choices=TYPE_CHOICES,default='ping')
    port = models.IntegerField(blank=True, null=True, help_text="مخصوص TCP/HTTP")
    expected_keyword = models.CharField(max_length=100, blank=True, null=True,help_text="مخصوص HTTP - کلمه مورد انتظار در پاسخ")
    is_active = models.BooleanField(default=True)
    check_interval = models.IntegerField(default=60, help_text="ثانیه")
    timeout = models.IntegerField(default=5, help_text="ثانیه")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_status = models.BooleanField(default=False, help_text="آخرین وضعیت ثبت شده")
    last_check_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_monitor_type_display()})"

    def get_monitor_type_display_fa(self):
        display_map = {
            'ping': 'پینگ',
            'http': 'HTTP/HTTPS',
            'tcp': 'پورت TCP',
            'dns': 'DNS',
        }
        return display_map.get(self.monitor_type, self.monitor_type)