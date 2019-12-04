"""REST API の各リソースの操作を行うリポジトリパターンのインターフェースを実装するモジュール

本モジュールは HTTP リクエストによる副作用を伴う。
本モジュールで実装したリポジトリを利用したテストを行う場合は
各クラスに対応するインターフェースを実装したモッククラスを実装して行うこと。
"""


from dialogapi.entity import Project
from dialogapi.entity import Bot
from dialogapi.entity import Application


class StatusCodeException(Exception):
    """期待したステータスコードでない場合に送出される例外クラス"""
    def set_status_code(self, status_code):
        self.status_code = status_code


def authorizer_header(user):
    headers = {"Authorization": user.access_token}
    return headers


def assert_status_code(expected_code, actual_code):
    """status code が期待した値と一致しない場合に例外を送出する関数"""
    if expected_code != actual_code:
        args = (expected_code, actual_code)
        msg = "Status code expected: {}, actual: {}".format(*args)
        exc = StatusCodeException(msg)
        exc.set_status_code(actual_code)
        raise exc


def _show_response(res):
    """デバッグ用関数"""
    print("request:")
    print("  method:",  res.request.method)
    print("  url:",     res.request.url)
    print("  headers:")
    for key, val in res.request.headers.items():
        print("    {}: {}".format(key, val))
    print("  body:",    res.request.body)
    print("response:")
    print("  status_code:", res.status_code)


class UserRepository:
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def login(self, user):
        """Management API でログインしてアクセストークンを払い出す

        Args:
            user (entity.User): ログインを行うユーザオブジェクト

        Returns:
            user (entity.User)
        """

        # パスワードがセットされていない場合は例外を出す
        if not user.password:
            raise Exception("Set password")

        # ログインエンドポイントの生成
        endpoint = self._endpoint.url("login")

        # ログイン
        data = {"accountName": user.name, "password": user.password}
        res = self._endpoint.requests.post(
            endpoint,
            json=data,
            headers=self._endpoint.header,
            timeout=3
        )
        assert_status_code(200, res.status_code)
        access_token = res.json()["accessToken"]

        # 認証完了の設定
        user.set_authorized(access_token=access_token)
        return user


class ProjectRepository:
    def __init__(self, endpoint, user):
        self._endpoint = endpoint
        self._user = user

    def get_all(self):
        """プロジェクト一覧を返す

        Args:
            user (User): ユーザオブジェクト

        Returns:
            List[project.Project]: サーバが管理するプロジェクト管理オブジェクトのリスト
        """
        endpoint = self._endpoint.url("projects")
        res = self._endpoint.requests.get(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(200, res.status_code)
        projects = [Project(name=item["projectName"],
                            id_=item["projectId"],
                            organization_id=item['organizationId'],
                            create_date=item['createDate'])
                    for item in res.json()["projects"]]
        return projects

    def get(self, project):
        projects = self.get_all()
        for project_ in projects:
            if project_.name == project.name:
                return project_
        raise Exception("Project {} not found".format(project.name))


class BotRepository:
    def __init__(self, endpoint, user, project):
        """
        Args:
            endpoint (str):
            user (User):
            project (Project):
        """
        self._endpoint = endpoint
        self._user = user
        self._project = project

    def get_all(self):
        endpoint = self._endpoint.url(
            "projects/{}/bots".format(self._project.id_)
        )
        res = self._endpoint.requests.get(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(200, res.status_code)

        bots = res.json()["bots"]
        if not bots:
            bots = []
        bots_ = [Bot(id_=item["botId"],
                     project=self,
                     scenario_project_id=item["scenarioProjectId"],
                     language=item["language"],
                     description=item["description"],
                     sraix=item["sraix"])
                 for item in bots]
        return bots_

    def get(self, bot):
        bots = self.get_all()
        for bot_ in bots:
            if bot_.id_ == bot.id_:
                return bot_
        raise Exception("Bot {} not found".format(bot.id_))

    def add(self, bot, ignore_sraix=False):
        try:
            self._add(bot=bot, ignore_sraix=False)
        except StatusCodeException as e:
            if e.status_code == 400:
                # v2.5を使っている場合はsraixを指定すると400のエラーが返る
                # # その場合に対応した処理
                print(
                    " Your platform seems to be NLU v2.5."
                    "Continue to setup bots without sraix option."
                )
                self._add(bot=bot, ignore_sraix=True)
            else:
                raise

    def _add(self, bot, ignore_sraix=False):
        endpoint = self._endpoint.url(
            "projects/{}/bots".format(self._project.id_)
        )
        data = {"botId": bot.id_,
                "scenarioProjectId": bot.scenario_project_id,
                "language": bot.language,
                "description": bot.description
                }

        if not ignore_sraix:
            data["sraix"] = bot.sraix

        res = self._endpoint.requests.post(
            endpoint,
            headers=authorizer_header(self._user),
            json=data
        )
        assert_status_code(201, res.status_code)

    def remove(self, bot):
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}".format(self._project.id_, bot.id_)
        )
        res = self._endpoint.requests.delete(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(204, res.status_code)

    def update(self, bot, ignore_sraix=False):
        """ボットの情報を更新する

        Args:
            bot (dialogapi.bot.Bot): 更新するボット
            ignore_sraix: (bool) True の場合、sraixの設定を反映しない。
                注意: NLU v2.5 の場合、sraixパラメータを付与するとエラーが発生するため、Falseに設定すること。

        Returns:
            None
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}".format(self._project.id_, bot.id_)
        )
        data = {"language": bot.language, "description": bot.description}
        if not ignore_sraix:
            data["sraix"] = bot.sraix

        res = self._endpoint.requests.put(
            endpoint,
            headers=authorizer_header(self._user),
            json=data
        )
        assert_status_code(204, res.status_code)

    def compile(self, bot):
        """ボットをコンパイルする

        Args:

        Returns:
            Dict[str][object]: HTTPレスポンスのJSONに対応する辞書オブジェクト
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/scenarios/compile".format(
                self._project.id_, bot.id_
            )
        )
        res = self._endpoint.requests.post(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(202, res.status_code)
        return res.json()

    def compile_status(self, bot):
        """ボットのコンパイル状態を取得する

        Args:

        Returns:
            bool: コンパイルが完了している場合は True を返す。
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/scenarios/compile/status".format(
                self._project.id_, bot.id_
            )
        )
        res = self._endpoint.requests.get(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(200, res.status_code)
        completed = res.json()["status"] == "Completed"
        return completed

    def transfer(self, bot):
        """ボットを転送する

        Args:

        Returns:
            Dict[str][object]: HTTPレスポンスのJSONに対応する辞書オブジェクト
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/scenarios/transfer".format(
                self._project.id_, bot.id_
            )
        )
        res = self._endpoint.requests.post(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(202, res.status_code)
        return res.json()

    def transfer_status(self, bot):
        """ボットの転送状態を取得する

        Args:

        Returns:
            Dict[str][object]: HTTPレスポンスのJSONに対応する辞書オブジェクト
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/scenarios/transfer/status".format(
                self._project.id_, bot.id_
            )
        )
        res = self._endpoint.requests.get(
            endpoint,
            headers=authorizer_header(self._user)
        )
        assert_status_code(200, res.status_code)
        completed = all(
            item["status"] == "Completed"
            for item in res.json()["transferStatusResponses"]
        )
        return completed


class AIMLRepository:
    def __init__(self, endpoint, user, project, bot):
        self._endpoint = endpoint
        self._user = user
        self._project = project
        self._bot = bot

    def upsert(self, aiml):
        """
        Args:
            aiml (AIML):
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/aiml".format(self._project.id_, self._bot.id_)
        )

        with open(aiml.filename, encoding="utf-8") as f:
            files = {"uploadFile": f}
            res = self._endpoint.requests.put(
                endpoint,
                headers=authorizer_header(self._user),
                files=files
            )

        if res.status_code != 201:
            try:
                print(res.json())
            except Exception:
                pass
            raise Exception("Status code {}".format(res.status_code))
        return res.status_code


class SetRepository:
    def __init__(self, endpoint, user, project, bot):
        self._endpoint = endpoint
        self._user = user
        self._project = project
        self._bot = bot

    def upsert(self, set):
        """
        Args:
            set (Set):
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/sets".format(self._project.id_, self._bot.id_)
        )

        with open(set.filename, encoding="utf-8") as f:
            files = {"uploadFile": f}
            res = self._endpoint.requests.put(
                endpoint,
                headers=authorizer_header(self._user),
                files=files
            )

        if res.status_code != 201:
            try:
                print(res.json())
            except Exception:
                pass
            raise Exception("Status code {}".format(res.status_code))
        return res.status_code


class MapRepository:
    def __init__(self, endpoint, user, project, bot):
        self._endpoint = endpoint
        self._user = user
        self._project = project
        self._bot = bot

    def upsert(self, map):
        """
        Args:
            set (Set):
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/maps".format(self._project.id_, self._bot.id_)
        )

        with open(map.filename, encoding="utf-8") as f:
            files = {"uploadFile": f}
            res = self._endpoint.requests.put(
                endpoint,
                headers=authorizer_header(self._user),
                files=files
            )

        if res.status_code != 201:
            try:
                print(res.json())
            except Exception:
                pass
            raise Exception("Status code {}".format(res.status_code))
        return res.status_code


class PropertyRepository:
    def __init__(self, endpoint, user, project, bot):
        self._endpoint = endpoint
        self._user = user
        self._project = project
        self._bot = bot

    def _add(self, property):
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/properties".format(
                self._project.id_, self._bot.id_
            )
        )
        res = self._endpoint.requests.post(
            endpoint,
            headers=authorizer_header(self._user),
            json=property.dict()
        )
        assert_status_code(201, res.status_code)

    def _update(self, property):
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/properties".format(
                self._project.id_, self._bot.id_
            )
        )
        res = self._endpoint.requests.put(
            endpoint,
            headers=authorizer_header(self._user),
            json=property.dict()
        )
        assert_status_code(204, res.status_code)

    def upsert(self, property):
            try:
                self._add(property)
            except StatusCodeException as e:
                # ボットプロパティが存在する場合は 409 がかえる
                if e.status_code == 409:
                    self._update(property)
                else:
                    raise


class ConfigRepository:
    def __init__(self, endpoint, user, project, bot):
        self._endpoint = endpoint
        self._user = user
        self._project = project
        self._bot = bot

    def upsert(self, config):
        """ボットのボットコンフィグを更新する

        Args:

        Returns:
            None
        """
        endpoint = self._endpoint.url(
            "projects/{}/bots/{}/configs".format(
                self._project.id_, self._bot.id_
            )
        )

        res = self._endpoint.requests.put(
            endpoint,
            headers=authorizer_header(self._user),
            json=config.dict()
        )
        assert_status_code(201, res.status_code)


class ApplicationRepository:
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def register(self, bot,
                 app_id=None, app_kind="dialogapi", notification="false"):
        endpoint = self._endpoint.url()

        data = {"bot_id": bot.id_,
                "app_kind": app_kind,
                "notification": notification}

        if app_id:
            data["app_id"] = app_id

        res = self._endpoint.requests.post(
            endpoint,
            headers=self._endpoint.header,
            json=data
        )
        assert_status_code(200, res.status_code)

        res_json = res.json()
        if "app_id" in res_json:
            app_id_ = res_json["app_id"]
        elif "appId" in res_json:
            app_id_ = res_json["appId"]
        else:
            raise Exception("appId not found in response json")

        return Application(bot=bot, app_id=app_id_)


class DialogueRepository:
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def dialogue(self, request):
        endpoint = self._endpoint.url()
        res = self._endpoint.requests.post(
            endpoint,
            headers=self._endpoint.header,
            json=request.dict()
        )
        assert_status_code(200, res.status_code)
        return res.json()
