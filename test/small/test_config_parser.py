import unittest
from dialogapi.config_parser import Parser
from dialogapi.config_parser import ParserException

YML = """
version: "1"

servers:
- name: test_server
  config:
    host: host.example.jp
    port: 443
    protocol: https
    ssl_verify: true
    user: ${USER}
    password: ${PASSWORD}
    endpoint:
      management:
        prefix: /management/v2.7
        header:
          content-type: application/json;charset=utf-8
      registration:
        prefix: /UserRegistrationServer/users/applications
        header:
          content-type: application/json;charset=utf-8
      dialogue:
        prefix: /SpontaneousDialogueServer/dialogue
        header:
          content-type: application/json;charset=utf-8

projects:
- name: TestProject
  config:
    project_name: PJ
  bots:
  - name: testBot
    config:
      bot_id: PJ_testBot
      description: テスト用
      sraix: global
      # 以下はデフォルトで割り当てられている
      # scenario_project_id: DSU
      # language: ja-JP
    configs:
    - sample/test.config
    properties:
    - sample/test.property
    aimls:
    - sample/test.aiml
    sets:
    - sample/test.set
    maps:
    - sample/test.map
"""


def build_config():
    context = {
        "USER": "TESTUSER",
        "PASSWORD": "TESTPASSWORD"
    }
    return Parser().parse_fd(YML, server="test_server", context=context)


class ParserTest(unittest.TestCase):
    def test_server_user(self):
        server, _ = build_config()
        user = server.user
        self.assertEqual(user.name, "TESTUSER")
        self.assertEqual(user.password, "TESTPASSWORD")

    def test_server_management_endpoint(self):
        server, _ = build_config()
        endpoint = server.management_endpoint
        self.assertEqual(
            endpoint.header,
            {"content-type": "application/json;charset=utf-8"}
        )
        self.assertEqual(
            endpoint.url("testend"),
            "https://host.example.jp:443/management/v2.7/testend"
        )

    def test_server_registration_endpoint(self):
        server, _ = build_config()
        endpoint = server.registration_endpoint
        self.assertEqual(
            endpoint.header,
            {"content-type": "application/json;charset=utf-8"}
        )
        self.assertEqual(
            endpoint.url("testend"),
            ("https://host.example.jp:443/"
             "UserRegistrationServer/users/applications/testend")
        )

    def test_server_dialogue_endpoint(self):
        server, _ = build_config()
        endpoint = server.dialogue_endpoint
        self.assertEqual(
            endpoint.header,
            {"content-type": "application/json;charset=utf-8"}
        )
        self.assertEqual(
            endpoint.url("testend"),
            ("https://host.example.jp:443/"
             "SpontaneousDialogueServer/dialogue/testend")
        )

    def test_bucket_get_project(self):
        _, bucket = build_config()
        project = bucket.get_project(project="TestProject")
        self.assertEqual(project.name, "PJ")

    def test_bucket_get_projects(self):
        _, bucket = build_config()
        projects = bucket.get_projects()
        self.assertEqual(len(projects), 1)
        project = projects[0]
        self.assertEqual(project.name, "PJ")

    def test_bucket_get_bot(self):
        _, bucket = build_config()
        bot = bucket.get_bot(
            project="TestProject",
            bot="testBot"
        )
        self.assertEqual(bot.id_, "PJ_testBot")

    def test_bucket_get_bots(self):
        _, bucket = build_config()
        bots = bucket.get_bots(project="TestProject")
        self.assertEqual(len(bots), 1)
        bot = bots[0]
        self.assertEqual(bot.id_, "PJ_testBot")
        self.assertEqual(bot.description, "テスト用")
        self.assertEqual(bot.sraix, "global")
        self.assertEqual(bot.scenario_project_id, "DSU")
        self.assertEqual(bot.language, "ja-JP")

    def _test_bot_related_methods(self, action, filename):
        _, bucket = build_config()
        aimls = getattr(bucket, action)(project="TestProject", bot="testBot")
        self.assertEqual(len(aimls), 1)
        aiml = aimls[0]
        self.assertEqual(aiml.filename, filename)

    def test_bucket_get_aimls(self):
        self._test_bot_related_methods("get_aimls", "sample/test.aiml")

    def test_bucket_get_sets(self):
        self._test_bot_related_methods("get_sets", "sample/test.set")

    def test_bucket_get_maps(self):
        self._test_bot_related_methods("get_maps", "sample/test.map")

    def test_bucket_get_configs(self):
        self._test_bot_related_methods("get_configs", "sample/test.config")

    def test_bucket_get_properties(self):
        self._test_bot_related_methods(
            "get_properties",
            "sample/test.property"
        )

    def test_bucket_get_tests(self):
        _, bucket = build_config()
        tests = bucket.get_tests(project="TestProject", bot="testBot")
        self.assertTrue(len(tests) >= 0)


class ParserExceptionTest(unittest.TestCase):
    """設定ファイルが誤っていた時にエラーの送出をチェックするテスト"""
    def setUp(self):
        self.YML = """
version: "1"

servers:
- name: test_server
  config:
    host: host.example.jp
    port: 443
    protocol: https
    ssl_verify: true
    user: ${USER}
    password: ${PASSWORD}
    endpoint:
      management:
        prefix: /management/v2.7
        header:
          content-type: application/json;charset=utf-8
      registration:
        prefix: /UserRegistrationServer/users/applications
        header:
          content-type: application/json;charset=utf-8
      dialogue:
        prefix: /SpontaneousDialogueServer/dialogue
        header:
          content-type: application/json;charset=utf-8

projects:
- name: TestProject
  config:
    project_name: PJ
  bots:
  - name: testBot
    config:
      bot_id: PJ_testBot
      description: テスト用
      sraix: global
      # 以下はデフォルトで割り当てられている
      # scenario_project_id: DSU
      # language: ja-JP
    configs:
    - sample/test.config
    properties:
    - sample/test.property
    aiml:  # ここのスペルが間違っている
    - sample/test.aiml
    sets:
    - sample/test.set
    maps:
    - sample/test.map
"""

    def test_build_exception(self):
        context = {
            "USER": "TESTUSER",
            "PASSWORD": "TESTPASSWORD"
        }
        with self.assertRaises(ParserException):
            Parser().parse_fd(
                self.YML,
                server="test_server",
                context=context
            )
