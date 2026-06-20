import time

from .utils import check_server_safe


class ServerMonitor:
    def __init__(self, retry_count=3, retry_delay=2):
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def check_with_retry(self, server):
        last_result = None
        for attempt in range(self.retry_count):
            last_result = check_server_safe(server)
            if last_result.get('status'):
                return last_result
            if attempt < self.retry_count - 1:
                time.sleep(self.retry_delay)
        return last_result
