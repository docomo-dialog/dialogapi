import unittest
from dialogapi.entity import Application
from dialogapi.entity import Bot
from dialogapi.test.method import AssertEqual
from dialogapi.test.method import AssertIn
from dialogapi.test.method import AssertRegexEqual
from dialogapi.test.method import AssertRegexIn
from dialogapi.test.method import AssertNotEqual
from dialogapi.test.method import AssertNotIn
from dialogapi.test.method import AssertRegexNotEqual
from dialogapi.test.method import AssertRegexNotIn
from dialogapi.test.method import AssertionMethodFactory
from dialogapi.test.task import Test
from dialogapi.test.task import Task
from dialogapi.test.task import TaskConfig
from dialogapi.test.task import TaskManager
from dialogapi.test.config import Parser


class ApplicationRepositoryMock:
    def register(self, bot):
        return Application(
            bot=bot,
            app_id="test_app_id"
        )


class DialogRepositoryMock:
    def dialogue(self, request):
        return {"systemText": {"expression": "ワールド"}}


class TaskManagerTest(unittest.TestCase):
    def test_execute_tasks_ok(self):
        # タスクの定義
        factory = AssertionMethodFactory()
        test = Test(method=factory.build("equal"),
                    param="response.systemText.expression",
                    expected="ワールド")
        task = Task(
            name="TaskManagerTest-tasks_ok",
            request={"voiceText": "ハロー"},
            tests=[test]
        )
        # タスクマネージャの定義
        manager = TaskManager(
            tasks=[task],
            config=TaskConfig(keep_app_id=False),
        )

        # 実行
        result = manager.execute_tasks(
            bot=Bot(id_="JP_testBot"),
            application_repository=ApplicationRepositoryMock(),
            dialogue_repository=DialogRepositoryMock()
        )
        self.assertTrue(result)


class TaskTest(unittest.TestCase):
    def test_execute_tests_ok(self):
        factory = AssertionMethodFactory()
        test = Test(method=factory.build("equal"),
                    param="response.systemText.expression",
                    expected="お疲れ様です。")
        # task の request の内容は内部でチェックしないので None を指定しておく
        task = Task(name="テストタスク", request=None, tests=[test])
        response = {
            "systemText": {
                "expression": "お疲れ様です。",
                "utterance": "おつかれさまです",
            },
            "dialogStatus": {},
            "serverSendTime": "2017-03-30 13:31:01",
        }
        res = task.execute_tests(response=response)
        self.assertTrue(res)

    def test_execute_tests_fail(self):
        factory = AssertionMethodFactory()
        test = Test(method=factory.build("equal"),
                    param="response.systemText.expression",
                    expected="お疲れ様です。")
        test2 = Test(method=factory.build("equal"),
                     param="response.systemText.expression",
                     expected="お疲れ様ですよね。")
        # task の request の内容は内部でチェックしないので None を指定しておく
        task = Task(name="テストタスク", request=None, tests=[test, test2])
        response = {
            "systemText": {
                "expression": "お疲れ様です。",
                "utterance": "おつかれさまです",
            },
            "dialogStatus": {},
            "serverSendTime": "2017-03-30 13:31:01",
        }
        res = task.execute_tests(response=response)
        self.assertFalse(res)


class TestTest(unittest.TestCase):
    def test_execute(self):
        factory = AssertionMethodFactory()
        test = Test(method=factory.build("equal"),
                    param="response.systemText.expression",
                    expected="お疲れ様です。")
        response = {
            "systemText": {
                "expression": "お疲れ様です。",
                "utterance": "おつかれさまです",
            },
            "dialogStatus": {},
            "serverSendTime": "2017-03-30 13:31:01",
        }
        res = test.execute(response=response)

        self.assertTrue(res.bool)
        self.assertEqual(res.result, "お疲れ様です。")
        self.assertEqual(res.expected, "お疲れ様です。")


class AssertionMethodFactoryTest(unittest.TestCase):
    def test_build_equal(self):
        factory = AssertionMethodFactory()
        cls = factory.build("equal")
        self.assertEqual(cls.__class__.__name__, "AssertEqual")

    def test_build_in(self):
        factory = AssertionMethodFactory()
        cls = factory.build("in")
        self.assertEqual(cls.__class__.__name__, "AssertIn")

    def test_build_regex_equal(self):
        factory = AssertionMethodFactory()
        cls = factory.build("regex_equal")
        self.assertEqual(cls.__class__.__name__, "AssertRegexEqual")

    def test_build_regex_in(self):
        factory = AssertionMethodFactory()
        cls = factory.build("regex_in")
        self.assertEqual(cls.__class__.__name__, "AssertRegexIn")

    def test_build_not_equal(self):
        factory = AssertionMethodFactory()
        cls = factory.build("not_equal")
        self.assertEqual(cls.__class__.__name__, "AssertNotEqual")

    def test_build_not_in(self):
        factory = AssertionMethodFactory()
        cls = factory.build("not_in")
        self.assertEqual(cls.__class__.__name__, "AssertNotIn")

    def test_build_regex_not_equal(self):
        factory = AssertionMethodFactory()
        cls = factory.build("regex_not_equal")
        self.assertEqual(cls.__class__.__name__, "AssertRegexNotEqual")

    def test_build_regex_not_in(self):
        factory = AssertionMethodFactory()
        cls = factory.build("regex_not_in")
        self.assertEqual(cls.__class__.__name__, "AssertRegexNotIn")


class AssertEqualTest(unittest.TestCase):
    def test_execute_true(self):
        method = AssertEqual()
        first = "テスト"
        second = "テスト"
        res = method.execute(first=first, second=second)
        self.assertTrue(res)

    def test_execute_false(self):
        method = AssertEqual()
        first = "テスト"
        second = "テスト1"
        res = method.execute(first=first, second=second)
        self.assertFalse(res)


class AssertInTests(unittest.TestCase):
    def test_execute_in(self):
        method = AssertIn()
        first = "テスト"
        second = ["テスト", "テスト2"]
        res = method.execute(first=first, second=second)
        self.assertTrue(res)

    def test_execute_not_in(self):
        method = AssertIn()
        first = "テスト"
        second = ["テスト1", "テスト2"]
        res = method.execute(first=first, second=second)
        self.assertFalse(res)


class AssertRegexEqualTest(unittest.TestCase):
    def test_execute_true(self):
        method = AssertRegexEqual()
        first = "テ スト"
        second = r"^\w "
        res = method.execute(first=first, second=second)
        self.assertTrue(res)

    def test_execute_false(self):
        method = AssertRegexEqual()
        first = "テ スト"
        second = r"か$"
        res = method.execute(first=first, second=second)
        self.assertFalse(res)


class AssertRegexInTest(unittest.TestCase):
    def test_execute_true(self):
        method = AssertRegexIn()
        first = "テ スト"
        second = ["感じ$", r"^\w "]
        res = method.execute(first=first, second=second)
        self.assertTrue(res)

    def test_execute_false(self):
        method = AssertRegexIn()
        first = "テ スト"
        second = ["感じ$", r"[はな]"]
        res = method.execute(first=first, second=second)
        self.assertFalse(res)


class AssertNotEqualTest(unittest.TestCase):
    def test_execute_false(self):
        method = AssertNotEqual()
        first = "テスト"
        second = "テスト"
        res = method.execute(first=first, second=second)
        self.assertFalse(res)

    def test_execute_true(self):
        method = AssertNotEqual()
        first = "テスト"
        second = "テスト1"
        res = method.execute(first=first, second=second)
        self.assertTrue(res)


class AssertNotInTests(unittest.TestCase):
    def test_execute_notin_false(self):
        method = AssertNotIn()
        first = "テスト"
        second = ["テスト", "テスト2"]
        res = method.execute(first=first, second=second)
        self.assertFalse(res)

    def test_execute_notin_true(self):
        method = AssertNotIn()
        first = "テスト"
        second = ["テスト1", "テスト2"]
        res = method.execute(first=first, second=second)
        self.assertTrue(res)


class AssertRegexNotEqualTest(unittest.TestCase):
    def test_execute_false(self):
        method = AssertRegexNotEqual()
        first = "テ スト"
        second = r"^\w "
        res = method.execute(first=first, second=second)
        self.assertFalse(res)

    def test_execute_true(self):
        method = AssertRegexNotEqual()
        first = "テ スト"
        second = r"か$"
        res = method.execute(first=first, second=second)
        self.assertTrue(res)


class AssertRegexNotInTest(unittest.TestCase):
    def test_execute_false(self):
        method = AssertRegexNotIn()
        first = "テ スト"
        second = ["感じ$", r"^\w "]
        res = method.execute(first=first, second=second)
        self.assertFalse(res)

    def test_execute_true(self):
        method = AssertRegexNotIn()
        first = "テ スト"
        second = ["感じ$", r"[はな]"]
        res = method.execute(first=first, second=second)
        self.assertTrue(res)


class TestParser(unittest.TestCase):
    def test_parse_fd(self):
        test_config = """
config:
  keep_app_id: true

tasks:
  - name: 「こんにちは」に対するテスト
    request:
      voiceText: こんにちは
      location:
        lat: 0
        lon: 0
      clientData:
        option:
          t: ols
    tests:
      - method: equal
        param: response.systemText.utterance
        expected: "こんにちは。"
      - method: in
        param: response.systemText.utterance
        expected:
        - "こんにちは。"
        - "こんにちは。元気ですか？"
      - method: equal
        param: response.command
        expected: "xheijfeiijf=="
  - name: 「はろー」に対するテスト
    request:
      voiceText: はろー
    tests:
      - method: equal
        param: response.systemText.utterance
        expected: "オンラインで変更済み"
        """
        manager = Parser().parse_fd(test_config)
        self.assertEqual(manager.tasks[0].name, "「こんにちは」に対するテスト")
        self.assertEqual(len(manager.tasks[0].tests), 3)
        self.assertEqual(manager.tasks[1].name, "「はろー」に対するテスト")
        self.assertEqual(len(manager.tasks[1].tests), 1)
