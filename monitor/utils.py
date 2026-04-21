import subprocess
import requests
import socket
from datetime import datetime


def check_ping(host, timeout=5):

    try:
        param = '-n' if subprocess.os.name == 'nt' else '-c'
        command = ['ping', param, '1', host]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def check_http(url, port=None, expected_keyword=None, timeout=5):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        if port:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            url = f"{parsed.scheme}://{parsed.hostname}:{port}{parsed.path or ''}"

        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        if response.status_code not in [200, 201, 301, 302, 307, 308]:
            return False

        if expected_keyword:
            return expected_keyword in response.text

        return True

    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False


def check_tcp(host, port, timeout=5):
    if not port:
        return False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def check_dns(host, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False
    except Exception:
        return False



def check_server(server):

    status = False
    response_time = None
    error_message = None

    try:
        import time
        start_time = time.time()

        if server.monitor_type == 'ping':
            status = check_ping(server.address, server.timeout)

        elif server.monitor_type == 'http':
            status = check_http(
                server.address,
                server.port,
                server.expected_keyword,
                server.timeout
            )

        elif server.monitor_type == 'tcp':
            if server.port:
                status = check_tcp(server.address, server.port, server.timeout)
            else:
                status = False
                error_message = "پورت مشخص نشده است"

        elif server.monitor_type == 'dns':
            status = check_dns(server.address, server.timeout)

        else:
            status = False
            error_message = "نوع مانیتورینگ نامعتبر"

        response_time = int((time.time() - start_time) * 1000)  # میلی‌ثانیه

    except Exception as e:
        status = False
        error_message = str(e)

    try:
        server.last_status = status
        server.last_check_time = datetime.now()
        server.save(update_fields=['last_status', 'last_check_time'])
    except Exception:
        pass

    return {
        'id': server.id,
        'name': server.name,
        'address': server.address,
        'port': server.port,
        'type': server.monitor_type,
        'type_display': server.get_monitor_type_display(),
        'status': status,
        'response_time': response_time,
        'last_check': server.last_check_time.strftime("%H:%M:%S") if server.last_check_time else None,
        'error_message': error_message,
    }



def check_multiple_servers(servers):

    results = []
    for server in servers:
        result = check_server(server)
        results.append(result)
    return results




def test_check(server_id):
    from .models import Server
    try:
        server = Server.objects.get(id=server_id)
        return check_server(server)
    except Server.DoesNotExist:
        return {'error': 'Server not found'}