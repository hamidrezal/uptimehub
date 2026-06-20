import re
import socket
import ssl
import subprocess
import time
from datetime import datetime, timezone as dt_timezone
from urllib.parse import urlparse

import requests
from django.utils import timezone

from .models import Server, ServerLog


def _base_result(server, status=False, response_time=None, error_message=None):
    return {
        'id': server.id,
        'name': server.name,
        'address': server.address,
        'port': server.port,
        'type': server.monitor_type,
        'type_display': server.get_monitor_type_display(),
        'status': status,
        'response_time': response_time,
        'last_check': timezone.localtime(server.last_check_time).strftime('%H:%M:%S') if server.last_check_time else None,
        'error_message': error_message,
        'ssl_expires_at': server.ssl_expires_at.isoformat() if server.ssl_expires_at else None,
        'domain_expires_at': server.domain_expires_at.isoformat() if server.domain_expires_at else None,
        'heartbeat_url': f'/heartbeat/{server.heartbeat_token}/' if server.monitor_type == Server.TYPE_HEARTBEAT else None,
    }


def _save_result(server, status, response_time=None, error_message=None, ssl_expires_at=None, domain_expires_at=None):
    old_status = server.last_status
    server.last_status = status
    server.last_response_time = response_time
    server.last_error_message = error_message
    server.last_check_time = timezone.now()
    if ssl_expires_at is not None:
        server.ssl_expires_at = ssl_expires_at
    if domain_expires_at is not None:
        server.domain_expires_at = domain_expires_at
    fields = ['last_status', 'last_response_time', 'last_error_message', 'last_check_time', 'updated_at']
    if ssl_expires_at is not None:
        fields.append('ssl_expires_at')
    if domain_expires_at is not None:
        fields.append('domain_expires_at')
    server.save(update_fields=fields)
    if old_status != status:
        ServerLog.objects.create(server=server, status=status, response_time=response_time, error_message=error_message or '')


def check_ping(host, timeout=5):
    param = '-n' if subprocess.os.name == 'nt' else '-c'
    completed = subprocess.run(['ping', param, '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return completed.returncode == 0, None if completed.returncode == 0 else 'Ping failed'


def check_tcp(host, port, timeout=5):
    if not port:
        return False, 'Port is required'
    with socket.create_connection((host, int(port)), timeout=timeout):
        return True, None


def check_dns(host, timeout=5):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        socket.getaddrinfo(host, None)
        return True, None
    finally:
        socket.setdefaulttimeout(old_timeout)


def _url_with_port(url, port):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    if not port:
        return url
    parsed = urlparse(url)
    netloc = parsed.hostname or ''
    if parsed.username:
        auth = parsed.username
        if parsed.password:
            auth += ':' + parsed.password
        netloc = auth + '@' + netloc
    netloc = f'{netloc}:{port}'
    return parsed._replace(netloc=netloc).geturl()


def check_http_like(server):
    url = _url_with_port(server.address, server.port)
    response = requests.request(
        method=server.http_method,
        url=url,
        headers=server.request_headers or {},
        data=server.request_body or None,
        timeout=server.timeout,
        allow_redirects=True,
    )
    if response.status_code not in server.expected_status_code_set():
        return False, f'Unexpected status code: {response.status_code}'
    if server.keyword_mode == 'contains' and (server.expected_keyword or '') not in response.text:
        return False, 'Expected text was not found in response'
    if server.keyword_mode == 'not_contains' and (server.expected_keyword or '') in response.text:
        return False, 'Blocked text was found in response'
    return True, None


def check_ssl(server):
    parsed = urlparse(server.address if '://' in server.address else 'https://' + server.address)
    host = parsed.hostname or server.address
    port = server.port or 443
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=server.timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
    expires_at = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=dt_timezone.utc)
    expires_at = timezone.datetime.fromtimestamp(expires_at.timestamp(), tz=dt_timezone.utc)
    days_left = (expires_at - timezone.now()).days
    if days_left < 0:
        return False, 'SSL certificate is expired', expires_at
    if days_left <= server.ssl_expiry_alert_days:
        return False, f'SSL certificate expires in {days_left} days', expires_at
    return True, None, expires_at


def _domain_from_address(address):
    parsed = urlparse(address if '://' in address else 'https://' + address)
    host = parsed.hostname or address
    return host.lower().strip('.')


def check_domain_expiry(server):
    domain = _domain_from_address(server.address)
    response = requests.get(f'https://rdap.org/domain/{domain}', timeout=server.timeout)
    if response.status_code >= 400:
        return False, f'RDAP lookup failed: {response.status_code}', None
    events = response.json().get('events', [])
    expiry_value = None
    for event in events:
        if event.get('eventAction') in {'expiration', 'expiry'}:
            expiry_value = event.get('eventDate')
            break
    if not expiry_value:
        return False, 'Domain expiry date not found in RDAP response', None
    expires_at = datetime.fromisoformat(expiry_value.replace('Z', '+00:00'))
    if timezone.is_naive(expires_at):
        expires_at = expires_at.replace(tzinfo=dt_timezone.utc)
    days_left = (expires_at - timezone.now()).days
    if days_left < 0:
        return False, 'Domain is expired', expires_at
    if days_left <= server.domain_expiry_alert_days:
        return False, f'Domain expires in {days_left} days', expires_at
    return True, None, expires_at


def check_heartbeat(server):
    if not server.last_heartbeat_at:
        return False, 'No heartbeat received yet'
    age = (timezone.now() - server.last_heartbeat_at).total_seconds()
    if age > server.heartbeat_grace_seconds:
        return False, f'Heartbeat is late by {int(age - server.heartbeat_grace_seconds)} seconds'
    return True, None


def check_server(server):
    start_time = time.monotonic()
    status = False
    error_message = None
    ssl_expires_at = None
    domain_expires_at = None
    try:
        if server.monitor_type == Server.TYPE_PING:
            status, error_message = check_ping(server.address, server.timeout)
        elif server.monitor_type in [Server.TYPE_HTTP, Server.TYPE_API]:
            status, error_message = check_http_like(server)
        elif server.monitor_type == Server.TYPE_TCP:
            status, error_message = check_tcp(server.address, server.port, server.timeout)
        elif server.monitor_type == Server.TYPE_DNS:
            status, error_message = check_dns(server.address, server.timeout)
        elif server.monitor_type == Server.TYPE_SSL:
            status, error_message, ssl_expires_at = check_ssl(server)
        elif server.monitor_type == Server.TYPE_DOMAIN:
            status, error_message, domain_expires_at = check_domain_expiry(server)
        elif server.monitor_type == Server.TYPE_HEARTBEAT:
            status, error_message = check_heartbeat(server)
        else:
            error_message = 'Invalid monitor type'
    except Exception as exc:
        status = False
        error_message = str(exc)

    response_time = int((time.monotonic() - start_time) * 1000)
    if status and server.max_response_time_ms and response_time > server.max_response_time_ms:
        status = False
        error_message = f'Response time {response_time}ms exceeded limit {server.max_response_time_ms}ms'

    _save_result(server, status, response_time, error_message, ssl_expires_at, domain_expires_at)
    return _base_result(server, status, response_time, error_message)


def check_server_safe(server):
    try:
        return check_server(server)
    except Exception as exc:
        return _base_result(server, False, None, str(exc))


def check_multiple_servers(servers):
    return [check_server(server) for server in servers]
