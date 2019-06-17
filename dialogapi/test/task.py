from dialogapi.entity import Request
from collections import namedtuple


class TaskConfig:
    def __init__(self, **argv):
        # パラメータのチェック
        keys = {"keep_app_id"}
        for key in argv:
            assert key in keys

        self.keep_app_id = argv.get("keep_app_id", False)


class TaskManager:
    """
    複数のタスクを制御するクラス
    """
    def __init__(self, tasks, config):
        self._tasks = tasks
        self._config = config

    @property
    def tasks(self):
        return self._tasks

    def execute_tasks(
        self, bot, application_repository,
        dialogue_repository
    ):
        results = []
        app = application_repository.register(bot=bot)
        for task in self._tasks:
            # keep_app_id が指定されていない場合、毎回app_idを新しく払い出す
            if not self._config.keep_app_id:
                app = application_repository.register(bot=bot)
            # dbot の app_id から新しくリクエストを生成する
            # - task.request に app_id が指定されていたら、そちらが優先される
            request = Request(
                application=app,
                voice_text=task.request["voiceText"],
                **{key: val for key, val in task.request.items()
                   if key != "voiceText"}
            )
            response = dialogue_repository.dialogue(request=request)
            res_bool = task.execute_tests(response=response)
            results.append(res_bool)
        return all(results)


class Task:
    def __init__(self, name, request, tests):
        """
        Args:
            name (str): タスク名
            request (Dict[str][Any]: 対話リクエスト
            tests (List[Test]): テストのリスト
        """
        self._name = name
        self._request = request
        self._tests = tests

    @property
    def name(self):
        return self._name

    @property
    def request(self):
        return self._request

    @property
    def tests(self):
        return self._tests

    def execute_tests(self, response):
        """
        Args:
            response (dict[str][Any]): 対話レスポンス
        """
        total_result = True
        for test in self._tests:
            print("- {} ...".format(self._name), end=" ")
            res = test.execute(response=response)
            if res.bool:
                print("ok.")
            else:
                print("fail.", end=" ")
                print(
                    ('In assertion method "{}", '
                     'result "{}" != expected "{}".').format(
                        test.method.name, res.result, res.expected
                    )
                )
                total_result = False

        return total_result


TestResult = namedtuple("TestResult", ["bool", "result", "expected"])


class Test:
    def __init__(self, method, param, expected):
        """
        Args:
            method (Assert): assertionメソッドクラスを指定する
            param (str): 利用するパラメータキー
                response.systemText.utterance
                のように、「.」でキーを指定する
            expected (str): 期待する応答
        """
        self._method = method
        self._param = param
        self._expected = expected

    @property
    def method(self):
        return self._method

    def execute(self, response):
        """
        Args:
            response (dict): dialogue API の応答辞書
        """
        keys = self._param.split(".")
        assert keys[0] == "response"
        keys = keys[1:]

        val = response
        for key in keys:
            val = val[key]
        return TestResult(
            bool=self._method.execute(val, self._expected),
            result=val,
            expected=self._expected
            )
