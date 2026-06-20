import json

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from monitor.models import Server

INPUT_CLASS = 'w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'


class ServerForm(forms.ModelForm):
    port = forms.IntegerField(required=False, validators=[MinValueValidator(1), MaxValueValidator(65535)], widget=forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '80, 443, 22'}))
    check_interval = forms.IntegerField(initial=60, min_value=30, max_value=86400, widget=forms.NumberInput(attrs={'class': INPUT_CLASS}))
    timeout = forms.IntegerField(initial=10, min_value=1, max_value=60, widget=forms.NumberInput(attrs={'class': INPUT_CLASS}))
    expected_keyword = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    request_body = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 4}))
    request_headers = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': '{"Authorization": "Bearer ..."}'}))

    class Meta:
        model = Server
        fields = [
            'name', 'address', 'monitor_type', 'port', 'is_active', 'check_interval', 'timeout',
            'http_method', 'request_headers', 'request_body', 'expected_status_codes',
            'keyword_mode', 'expected_keyword', 'max_response_time_ms',
            'ssl_expiry_alert_days', 'domain_expiry_alert_days', 'heartbeat_grace_seconds',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '\u0633\u0627\u06cc\u062a \u0627\u0635\u0644\u06cc'}),
            'address': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://example.com ?? 8.8.8.8'}),
            'monitor_type': forms.Select(attrs={'class': INPUT_CLASS}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500'}),
            'http_method': forms.Select(attrs={'class': INPUT_CLASS}),
            'expected_status_codes': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '200,201,204'}),
            'keyword_mode': forms.Select(attrs={'class': INPUT_CLASS}),
            'max_response_time_ms': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '1000'}),
            'ssl_expiry_alert_days': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'domain_expiry_alert_days': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'heartbeat_grace_seconds': forms.NumberInput(attrs={'class': INPUT_CLASS}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'name': '\u0646\u0627\u0645 \u0645\u0627\u0646\u06cc\u062a\u0648\u0631',
            'address': '\u0622\u062f\u0631\u0633 / \u062f\u0627\u0645\u0646\u0647 / IP / Endpoint',
            'monitor_type': '\u0646\u0648\u0639 \u0645\u0627\u0646\u06cc\u062a\u0648\u0631\u06cc\u0646\u06af',
            'port': '\u067e\u0648\u0631\u062a',
            'is_active': '\u0641\u0639\u0627\u0644 \u0628\u0627\u0634\u062f',
            'check_interval': '\u0641\u0627\u0635\u0644\u0647 \u0628\u0631\u0631\u0633\u06cc (\u062b\u0627\u0646\u06cc\u0647)',
            'timeout': '\u062a\u0627\u06cc\u0645 \u0627\u0648\u062a (\u062b\u0627\u0646\u06cc\u0647)',
            'http_method': '\u0645\u062a\u062f HTTP/API',
            'request_headers': 'Headers \u062f\u0631\u062e\u0648\u0627\u0633\u062a (JSON)',
            'request_body': 'Body \u062f\u0631\u062e\u0648\u0627\u0633\u062a',
            'expected_status_codes': '\u0627\u0633\u062a\u062a\u0648\u0633 \u06a9\u062f\u0647\u0627\u06cc \u0645\u0648\u0631\u062f \u0642\u0628\u0648\u0644',
            'keyword_mode': '\u0628\u0631\u0631\u0633\u06cc \u0645\u062a\u0646 \u062f\u0631 \u067e\u0627\u0633\u062e',
            'expected_keyword': '\u0645\u062a\u0646 \u0645\u0648\u0631\u062f \u0628\u0631\u0631\u0633\u06cc',
            'max_response_time_ms': '\u062d\u062f\u0627\u06a9\u062b\u0631 Response Time (\u0645\u06cc\u0644\u06cc \u062b\u0627\u0646\u06cc\u0647)',
            'ssl_expiry_alert_days': '\u0647\u0634\u062f\u0627\u0631 \u0627\u0646\u0642\u0636\u0627\u06cc SSL (\u0631\u0648\u0632 \u0642\u0628\u0644)',
            'domain_expiry_alert_days': '\u0647\u0634\u062f\u0627\u0631 \u0627\u0646\u0642\u0636\u0627\u06cc \u062f\u0627\u0645\u0646\u0647 (\u0631\u0648\u0632 \u0642\u0628\u0644)',
            'heartbeat_grace_seconds': '\u0645\u0647\u0644\u062a Heartbeat (\u062b\u0627\u0646\u06cc\u0647)',
        }
        help_texts = {
            'monitor_type': '\u0647\u0645\u0647 \u06af\u0632\u06cc\u0646\u0647\u200c\u0647\u0627\u06cc \u062f\u0631\u062e\u0648\u0627\u0633\u062a\u06cc: HTTP/HTTPS\u060c Ping\u060c TCP Port\u060c DNS\u060c SSL\u060c Heartbeat\u060c API Endpoint\u060c Domain Expiry',
            'check_interval': '\u0645\u062b\u0627\u0644: 30\u060c 60\u060c 300',
            'expected_status_codes': '\u0645\u062b\u0627\u0644: 200 \u06cc\u0627 200,201,204',
            'keyword_mode': '\u0645\u06cc\u200c\u062a\u0648\u0627\u0646\u06cc\u062f \u0648\u062c\u0648\u062f \u06cc\u0627 \u0646\u0628\u0648\u062f \u06cc\u06a9 \u0645\u062a\u0646 \u062e\u0627\u0635 \u0631\u0627 \u062f\u0631 \u067e\u0627\u0633\u062e \u0686\u06a9 \u06a9\u0646\u06cc\u062f.',
            'heartbeat_grace_seconds': '\u0627\u06af\u0631 Cron Job \u062f\u0631 \u0627\u06cc\u0646 \u0645\u062f\u062a \u062f\u0631\u062e\u0648\u0627\u0633\u062a \u0646\u0632\u0646\u062f\u060c Down \u0645\u06cc\u200c\u0634\u0648\u062f.',
        }
        for name, label in labels.items():
            self.fields[name].label = label
        for name, help_text in help_texts.items():
            self.fields[name].help_text = help_text

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
