import yaml
from .task import TaskConfig
from .task import TaskManager
from .task import Task
from .task import Test
from .method import AssertionMethodFactory


"""テスト設定ファイル解析モジュール

# テストファイルの例

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
"""


class Parser:
    def parse(self, filename):
        with open(filename) as f:
            content = f.read()
        return self.parse_fd(content)

    def parse_fd(self, content):
        """
        Args:
            content (str): YAML文字列
        Returns:
            (TaskManager): タスクマネージャ
        """
        yaml_dic = yaml.load(content)

        factory = AssertionMethodFactory()
        tasks = []
        for taskdic in yaml_dic["tasks"]:
            task_name = taskdic["name"]
            task_request = taskdic["request"]
            tests = []
            for testdic in taskdic["tests"]:
                test = Test(method=factory.build(testdic["method"]),
                            param=testdic["param"],
                            expected=testdic["expected"])
                tests.append(test)
            task = Task(name=task_name, request=task_request, tests=tests)
            tasks.append(task)

        # タスクマネージャの定義
        manager = TaskManager(
            tasks=tasks,
            config=TaskConfig(**yaml_dic["config"])
        )
        return manager
