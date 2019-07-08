class User:
    """ユーザ管理クラス"""
    def __init__(self, name, password=None, access_token=None):
        """
        Args:
            name (str): ユーザ名
            password (str): パスワード
            access_token (str): APIへのアクセストークン
        """
        self._name = name
        self._password = password
        self._access_token = access_token
        # access_token が指定された場合 authorized に True をセットする
        self._authorized = True if access_token else False

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def access_token(self):
        return self._access_token

    @property
    def authorized(self):
        return self._authorized

    def set_authorized(self, access_token):
        """認証が成功した場合に呼び出すメソッドで、
        - authorized を True にセット
        - access_token に トークンをセット
        する

        Args:
            access_token (str): アクセストークン

        Returns:
            None
        """
        self._authorized = True
        self._access_token = access_token


class Project:
    """プロジェクト管理クラス"""
    def __init__(self, name,
                 id_=None, organization_id=None, create_date=None):
        """
        Args:
            name (str): プロジェクト名
            id_ (str): プロジェクトID。指定しない場合は None とする
            organization_id (str): 組織ID。指定しない場合は None とする
            create_date (str): プロジェクト作成美。指定しない場合は None とする
        """
        self._id_ = id_
        self._name = name
        self._organization_id = organization_id
        self._create_date = create_date

    @property
    def name(self):
        return self._name

    @property
    def id_(self):
        return self._id_


class Bot:
    def __init__(self, id_,
                 project=None,
                 scenario_project_id="DSU",
                 language="ja-JP",
                 description="",
                 sraix="null"):
        """
        Args:
            id_ (str): ボットID
            project (project.Project): Botを保持するプロジェクト管理オブジェクト
            scenario_project_id (str): project.name とは別物。「DSU」で固定して使う
            language (str): 言語
            description (str): 説明
            sraix (str): sraixの設定値。null, public, global を受け取る
        """
        self._id_ = id_
        self._project = project
        self._scenario_project_id = scenario_project_id
        self._language = language
        self._description = description
        assert sraix in {"null", "public", "global"}
        self._sraix = sraix

    @property
    def id_(self):
        return self._id_

    @property
    def project(self):
        return self._project

    @property
    def scenario_project_id(self):
        return self._scenario_project_id

    @property
    def language(self):
        return self._language

    @property
    def description(self):
        return self._description

    @property
    def sraix(self):
        return self._sraix


class _FileResource:
    """ファイルに依存したリソースクラス。継承して利用する"""
    def __init__(self, filename):
        self._filename = filename

    @property
    def filename(self):
        return self._filename


class AIML(_FileResource):
    """AIML管理クラス"""


class Set(_FileResource):
    """Set管理クラス"""


class Map(_FileResource):
    """Map管理クラス"""


class _KeyValueResource:
    """キー値型のファイルに依存したリソースクラス。継承して利用する

    キー値型のファイルは次の形式で "=" で接続して記述する

        key1=value1
        key2=value2
    """
    def __init__(self, filename):
        """
        Args:
            filename (str): 設定ファイル名
        """
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    def dict(self):
        cdict = dict()
        with open(self._filename, encoding="utf-8") as f:
            for line in f:
                key, val = line.strip("\n").split("=")
                cdict[key] = val
        return cdict


class Property(_KeyValueResource):
    """ボットプロパティの管理クラス"""


class Config(_KeyValueResource):
    """ボットコンフィグの管理クラス"""


class Application:
    def __init__(self, bot, app_id):
        self._bot = bot
        self._app_id = app_id

    @property
    def bot(self):
        return self._bot

    @property
    def app_id(self):
        return self._app_id


class Request:
    def __init__(self, application, voice_text, **argv):
        """対話リクエスト
        Params:
            application (Application): アプリケーション
            voice_text (str): 入力発話
            argv (dict): voiceText, botId, appId 以外のパラメータを指定する。
        """
        # リクエストの必須パラメータ
        self._REQUIRED_PARAMS = {
            "voiceText",  # Type: str
            "language",   # Type: str
            "botId",      # Type: str
            "appId",      # Type: str
        }
        # リクエストのオプションパラメータ
        self._OPTION_PARAMS = {
            # オプションパラメータ
            "clientVer",        # Type: str
            "initTalkingFlag",  # Type: bool
            "initTopicId",      # Type: str
            "initThat",         # Type: str
            "location",         # Type: dict, {"lat": 0, "lon": 0}
            "clientData",       # Type: dict
            "appRecvTime",      # Type: str, YYYY-MM-DD hh:mm:ss 形式
            "addSendTime",      # Type: str, YYYY-MM-DD hh:mm:ss 形式
            "projectSpecific",  # Type: Any
        }

        # 必須パラメータの設定
        self._dic = dict()
        self._dic["voiceText"] = voice_text
        self._dic["language"] = argv.get("language", "ja-JP")
        self._dic["botId"] = application.bot.id_
        self._dic["appId"] = application.app_id

        # オプションパラメータの設定
        for option_key in self._OPTION_PARAMS:
            if option_key in argv:
                self._dic[option_key] = argv[option_key]

    def dict(self):
        return self._dic
