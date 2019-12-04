import requests
import urllib3

# SSLでの検証を無効化した場合に Warning を非表示にする
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requests:
    def __init__(self, verify):
        self._verify = verify

    @property
    def verify(self):
        return self._verify

    def __getattr__(self, name):
        def decorate(callble):
            def func(*args, **kwargs):
                return callble(*args, **kwargs, verify=self._verify)
            return func

        return decorate(getattr(requests, name))
