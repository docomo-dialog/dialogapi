import unittest
from dialogapi.server import Server
from dialogapi.server import Endpoint
from dialogapi.server import EndpointException
from dialogapi.entity import User


def build_endpoint():
    host = "host.example.jp"
    port = 10443
    protocol = "https"
    prefix = "/management"
    header = {"content-type": "management"}
    ssl_verify = True
    url = "{}://{}:{}{}".format(protocol, host, port, prefix)

    endpoint = Endpoint(
        host=host,
        port=port,
        protocol=protocol,
        prefix=prefix,
        ssl_verify=ssl_verify,
        header=header
    )

    return endpoint, header, url, ssl_verify


class EndpointTest(unittest.TestCase):
    def test_properties(self):
        endpoint, header, url, ssl_verify = build_endpoint()
        self.assertEqual(endpoint.header, header)
        self.assertEqual(endpoint.url(), url)
        self.assertEqual(endpoint.ssl_verify, ssl_verify)
        self.assertEqual(endpoint.requests.verify, ssl_verify)


class ServerTest(unittest.TestCase):
    def test_management_endpoint(self):
        user = User(name="TestUser")
        server = Server(
            management_endpoint=build_endpoint()[0],
            registration_endpoint=None,
            dialogue_endpoint=None,
            user=user,
            ssl_verify=True
        )
        self.assertEqual(
            server.management_endpoint.url(),
            "https://host.example.jp:10443/management"
        )

        with self.assertRaises(EndpointException):
            server.registration_endpoint

        with self.assertRaises(EndpointException):
            server.dialogue_endpoint

    def test_registration_endpoint(self):
        user = User(name="TestUser")
        server = Server(
            management_endpoint=None,
            registration_endpoint=build_endpoint()[0],
            dialogue_endpoint=None,
            user=user,
            ssl_verify=True
        )
        self.assertEqual(
            server.registration_endpoint.url(),
            "https://host.example.jp:10443/management"
        )

        with self.assertRaises(EndpointException):
            server.management_endpoint

        with self.assertRaises(EndpointException):
            server.dialogue_endpoint

    def test_dialogue_endpoint(self):
        user = User(name="TestUser")
        server = Server(
            management_endpoint=None,
            registration_endpoint=None,
            dialogue_endpoint=build_endpoint()[0],
            user=user,
            ssl_verify=True
        )
        self.assertEqual(
            server.dialogue_endpoint.url(),
            "https://host.example.jp:10443/management"
        )

        with self.assertRaises(EndpointException):
            server.management_endpoint

        with self.assertRaises(EndpointException):
            server.registration_endpoint


class PropertyTest(unittest.TestCase):
    def test_header(self):
        endpoint, header, _ = build_endpoint()[:3]
        self.assertEqual(endpoint.header, header)

    def test_url(self):
        endpoint, _, url = build_endpoint()[:3]
        self.assertEqual(endpoint.url(), url)

    def test_url_with_point(self):
        endpoint, _, url = build_endpoint()[:3]
        self.assertEqual(endpoint.url("test"), url + "/test")
