from django import forms
from monitor.models import Server
from django.core.validators import MinValueValidator, MaxValueValidator



class ServerForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'google.com یا 8.8.8.8 یا https://mysite.com'
        })
    )

    port = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'مثال: 80, 443, 22'
        })
    )

    expected_keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'کلمه مورد نظر در پاسخ'
        })
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'مثال: سرور اصلی من'
        })
    )

    check_interval = forms.IntegerField(
        initial=60,
        min_value=10,
        max_value=3600,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    timeout = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500'
        })
    )

    monitor_type = forms.ChoiceField(
        choices=Server.TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    class Meta:
        model = Server
        fields = [
            'name', 'address', 'monitor_type', 'port',
            'expected_keyword', 'check_interval', 'timeout', 'is_active'
        ]

    def clean(self):
        cleaned_data = super().clean()
        monitor_type = cleaned_data.get('monitor_type')
        port = cleaned_data.get('port')
        expected_keyword = cleaned_data.get('expected_keyword')

        if monitor_type in ['http', 'tcp'] and not port:
            self.add_error('port', 'برای نوع HTTP/HTTPS و TCP وارد کردن پورت الزامی است')

        if monitor_type == 'http' and expected_keyword:
            if len(expected_keyword) < 2:
                self.add_error('expected_keyword', 'کلمه مورد نظر باید حداقل ۲ کاراکتر باشد')

        return cleaned_data

    def clean_address(self):
        address = self.cleaned_data.get('address')
        monitor_type = self.cleaned_data.get('monitor_type')

        if monitor_type == 'http':
            if not address.startswith(('http://', 'https://')):
                address = 'https://' + address

        return address