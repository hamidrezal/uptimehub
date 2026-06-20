import json

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from monitor.models import Server


INPUT_CLASS = (
    'w-full px-4 py-2.5 rounded-xl '
    'bg-navy-800 border border-navy-600 '
    'text-white placeholder-slate2 '
    'focus:outline-none focus:border-teal focus:ring-2 focus:ring-teal/20 '
    'transition-colors'
)

SELECT_CLASS = (
    'w-full px-4 py-2.5 rounded-xl '
    'bg-navy-800 border border-navy-600 '
    'text-white '
    'focus:outline-none focus:border-teal focus:ring-2 focus:ring-teal/20 '
    'transition-colors'
)

TEXTAREA_CLASS = (
    'w-full px-4 py-2.5 rounded-xl '
    'bg-navy-800 border border-navy-600 '
    'text-white placeholder-slate2 '
    'focus:outline-none focus:border-teal focus:ring-2 focus:ring-teal/20 '
    'transition-colors resize-none font-mono text-sm'
)

CHECKBOX_CLASS = (
    'w-4 h-4 rounded '
    'bg-navy-800 border-navy-600 '
    'text-teal focus:ring-teal focus:ring-offset-0'
)


class ServerForm(forms.ModelForm):
    port = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '80, 443, 22',
        })
    )

    check_interval = forms.IntegerField(
        initial=60,
        min_value=30,
        max_value=86400,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
        })
    )

    timeout = forms.IntegerField(
        initial=10,
        min_value=1,
        max_value=60,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
        })
    )

    expected_keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'متنی که باید در پاسخ بررسی شود',
        })
    )

    request_body = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': TEXTAREA_CLASS,
            'rows': 4,
            'placeholder': '{"key": "value"}',
        })
    )

    request_headers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': TEXTAREA_CLASS,
            'rows': 3,
            'placeholder': '{"Authorization": "Bearer ..."}',
        })
    )

    class Meta:
        model = Server
        fields = [
            'name',
            'address',
            'monitor_type',
            'port',
            'is_active',
            'check_interval',
            'timeout',
            'http_method',
            'request_headers',
            'request_body',
            'expected_status_codes',
            'keyword_mode',
            'expected_keyword',
            'max_response_time_ms',
            'ssl_expiry_alert_days',
            'domain_expiry_alert_days',
            'heartbeat_grace_seconds',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'سایت اصلی',
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'https://example.com یا 8.8.8.8',
                'dir': 'ltr',
            }),
            'monitor_type': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': CHECKBOX_CLASS,
            }),
            'http_method': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
            'expected_status_codes': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '200,201,204',
                'dir': 'ltr',
            }),
            'keyword_mode': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
            'max_response_time_ms': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '1000',
            }),
            'ssl_expiry_alert_days': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'domain_expiry_alert_days': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'heartbeat_grace_seconds': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = {
            'name': 'نام مانیتور',
            'address': 'آدرس / دامنه / IP / Endpoint',
            'monitor_type': 'نوع مانیتورینگ',
            'port': 'پورت',
            'is_active': 'فعال باشد',
            'check_interval': 'فاصله بررسی (ثانیه)',
            'timeout': 'تایم اوت (ثانیه)',
            'http_method': 'متد HTTP/API',
            'request_headers': 'Headers درخواست (JSON)',
            'request_body': 'Body درخواست',
            'expected_status_codes': 'استتوس کدهای مورد قبول',
            'keyword_mode': 'بررسی متن در پاسخ',
            'expected_keyword': 'متن مورد بررسی',
            'max_response_time_ms': 'حداکثر Response Time (میلی ثانیه)',
            'ssl_expiry_alert_days': 'هشدار انقضای SSL (روز قبل)',
            'domain_expiry_alert_days': 'هشدار انقضای دامنه (روز قبل)',
            'heartbeat_grace_seconds': 'مهلت Heartbeat (ثانیه)',
        }

        help_texts = {
            'monitor_type': 'HTTP/HTTPS، Ping، TCP Port، DNS، SSL، Heartbeat، API Endpoint و Domain Expiry',
            'check_interval': 'مثال: 30، 60، 300',
            'expected_status_codes': 'مثال: 200 یا 200,201,204',
            'keyword_mode': 'می‌توانید وجود یا نبود یک متن خاص را در پاسخ بررسی کنید.',
            'heartbeat_grace_seconds': 'اگر Cron Job در این مدت درخواست نزند، Down می‌شود.',
        }

        for name, label in labels.items():
            self.fields[name].label = label

        for name, help_text in help_texts.items():
            self.fields[name].help_text = help_text

        for field in self.fields.values():
            field.widget.attrs.setdefault('autocomplete', 'off')

    def clean_request_headers(self):
        value = self.cleaned_data.get('request_headers')

        if not value:
            return None

        if isinstance(value, dict):
            return value

        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError('Headers باید JSON معتبر باشد.') from exc

        if not isinstance(parsed, dict):
            raise forms.ValidationError('Headers باید یک object JSON باشد.')

        return parsed

    def clean_expected_status_codes(self):
        value = self.cleaned_data.get('expected_status_codes') or '200'
        codes = [part.strip() for part in value.split(',') if part.strip()]

        if not codes or any(not item.isdigit() for item in codes):
            raise forms.ValidationError('Status codeها را با عدد و کاما وارد کنید؛ مثل 200,201.')

        return ','.join(codes)

    def clean(self):
        cleaned_data = super().clean()
        monitor_type = cleaned_data.get('monitor_type')
        port = cleaned_data.get('port')
        keyword_mode = cleaned_data.get('keyword_mode')
        expected_keyword = cleaned_data.get('expected_keyword')

        if monitor_type == Server.TYPE_TCP and not port:
            self.add_error('port', 'برای مانیتور TCP وارد کردن پورت الزامی است.')

        if monitor_type == Server.TYPE_SSL and port is None:
            cleaned_data['port'] = 443

        if monitor_type in [Server.TYPE_HTTP, Server.TYPE_API] and not (cleaned_data.get('address') or '').startswith(('http://', 'https://')):
            cleaned_data['address'] = 'https://' + cleaned_data.get('address', '')

        if keyword_mode in ['contains', 'not_contains'] and not expected_keyword:
            self.add_error('expected_keyword', 'برای بررسی متن، مقدار متن را وارد کنید.')

        return cleaned_data