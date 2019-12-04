import unittest
from dialogapi.requests import Requests


class RequestsTest(unittest.TestCase):
    def test_method_call(self):
        url = "https://www.nttdocomo.co.jp/"
        res = Requests(verify=True).get(url)
        self.assertEqual(res.status_code, 200)
