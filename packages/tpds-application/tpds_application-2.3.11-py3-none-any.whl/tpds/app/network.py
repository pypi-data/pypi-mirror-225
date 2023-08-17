import requests

from PySide6.QtCore import QThreadPool

from tpds.worker import Worker

class NetworkTools():
    def __init__(self):
        pass

    @staticmethod
    def network_check():
        urls_to_ping = [
            "https://www.google.com/",      "https://www.google.com.hk/",
            "https://github.com/",          "https://gitee.com/",
            "https://www.microchip.com/"]
        for url in urls_to_ping:
            try:
                r = requests.head(url, timeout=3)
                return True
            except requests.ConnectionError as ex:
                pass
        return False

    def network_check_thread(self, fn):
        self.worker_obj = Worker(self.network_check)
        self.worker_obj.signals.result.connect(fn)
        QThreadPool.globalInstance().start(self.worker_obj)
