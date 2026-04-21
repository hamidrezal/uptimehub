from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره موبایل")
    is_premium = models.BooleanField(default=False, verbose_name="کاربر ویژه")
    email_notifications = models.BooleanField(default=True, verbose_name="اعلان ایمیل")
    telegram_notifications = models.BooleanField(default=False, verbose_name="اعلان تلگرام")
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="آیدی تلگرام")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username