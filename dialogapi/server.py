"""APIのエンドポイントとユーザを管理するモジュール"""

from dialogapi.requests import Requests


class EndpointException(Exception):
    """不正なエンドポイントが指定された時に送出される例外"""


class Endpoint:
    """APIのエンドポイントを表すクラス"""
    def __init__(self, host, port, protocol, prefix, header, ssl_verify):
        self._host = host
        self._port = port
        self._protocol = protocol
        self._prefix = prefix
        self._header = header
        self._ssl_verify = ssl_verify

    @property
    def header(self):
        return self._header

    @property
    def ssl_verify(self):
        return self._ssl_verify

    @property
    def requests(self, *args, **argv):
        return Requests(verify=self._ssl_verify)

    def url(self, point=None):
        args = (self._protocol, self._host, self._port, self._prefix)
        path = "{}://{}:{}{}".format(*args)
        if point:
            path = "{}/{}".format(path, point)
        return path


class Server:
    """APIのエンドポイントとユーザを管理するクラス"""
    def __init__(
        self, management_endpoint, registration_endpoint, dialogue_endpoint,
        user, ssl_verify
    ):
        self._management_endpoint = management_endpoint
        self._registration_endpoint = registration_endpoint
        self._dialogue_endpoint = dialogue_endpoint
        self._user = user
        self._ssl_verify = ssl_verify

    @property
    def user(self):
        return self._user

    @property
    def management_endpoint(self):
        return self._verify_exist(self._management_endpoint, "management")

    @property
    def registration_endpoint(self):
        return self._verify_exist(self._registration_endpoint, "registration")

    @property
    def dialogue_endpoint(self):
        return self._verify_exist(self._dialogue_endpoint, "dialogue")

    def _verify_exist(self, endpoint, type_):
        if not endpoint:
            raise EndpointException(
                "This server doesn't have {} endpoint".format(type_)
            )
        return endpoint
