import requests as _requests
import urllib3

# SSLでの検証を無効化した場合に Warning を非表示にする
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requests:
    def __init__(self, verify=None):
        self._verify = verify

    def set_verify(self, verify):
        self._verify = verify

    def __getattr__(self, name):
        def decorate(callble):
            def func(*args, **kwargs):
                return callble(*args, **kwargs, verify=self._verify)
            return func

        return decorate(getattr(_requests, name))


requests = Requests()
