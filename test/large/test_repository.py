import unittest
import os
from dialogapi.server import Endpoint
from dialogapi.repository import StatusCodeException
from dialogapi.repository import UserRepository
from dialogapi.repository import ProjectRepository
from dialogapi.repository import BotRepository
from dialogapi.repository import AIMLRepository
from dialogapi.repository import SetRepository
from dialogapi.repository import MapRepository
from dialogapi.repository import PropertyRepository
from dialogapi.repository import ConfigRepository
from dialogapi.repository import ApplicationRepository
from dialogapi.repository import DialogueRepository
from dialogapi.repository import assert_status_code
from dialogapi.entity import User
from dialogapi.entity import Project
from dialogapi.entity import Bot
from dialogapi.entity import AIML
from dialogapi.entity import Set
from dialogapi.entity import Map
from dialogapi.entity import Property
from dialogapi.entity import Config
from dialogapi.entity import Request


# Define external endpoint
PROTOCOL = "https"
PORT = "10443"
HOST = os.environ["HOST"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
PROJECT = os.environ["PROJECT"]

MANAGEMENT_ENDPOINT = Endpoint(
    host=HOST, port=PORT, protocol=PROTOCOL,
    prefix="/NLPManagementAPI",
    header={"content-type": "application/json;charset=utf-8"}
)
REGISTRATION_ENDPOINT = Endpoint(
    host=HOST, port=PORT, protocol=PROTOCOL,
    prefix="/UserRegistrationServer/users/applications",
    header={"content-type": "application/json;charset=utf-8"}
)
DIALOGUE_ENDPOINT = Endpoint(
    host=HOST, port=PORT, protocol=PROTOCOL,
    prefix="/SpontaneousDialogueServer/dialogue",
    header={"content-type": "application/json;charset=utf-8"}
)


# Factory functions
def get_login_user():
    repos = UserRepository(endpoint=MANAGEMENT_ENDPOINT)
    user = User(name=USER, password=PASSWORD)
    login_user = repos.login(user=user)
    return login_user


def get_project():
    return Project(name=PROJECT, id_=11)


def get_project_repository():
    login_user = get_login_user()
    repos = ProjectRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user
    )
    return repos


def get_bot():
    return Bot(id_="{}_test".format(PROJECT))


def get_bot_repository():
    login_user = get_login_user()
    project = get_project()
    repos = BotRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project
    )
    return repos


class BotInitializer:
    """使用している間だけボットを存在させる with 文を実装したクラス"""
    def __enter__(self):
        repos = get_bot_repository()
        bot = get_bot()
        try:
            repos.remove(bot=bot)
        except StatusCodeException:
            pass
        repos.add(bot=bot)
        return bot

    def __exit__(self, exc_type, exc_value, traceback):
        repos = get_bot_repository()
        bot = get_bot()
        repos.remove(bot=bot)


def _abspath(filename):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename
    )


def get_aiml():
    return AIML(_abspath("./test.aiml"))


def get_aiml_repository():
    login_user = get_login_user()
    project = get_project()
    bot = get_bot()
    repos = AIMLRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project,
        bot=bot
    )
    return repos


def get_set():
    return Set(_abspath("./test.set"))


def get_set_repository():
    login_user = get_login_user()
    project = get_project()
    bot = get_bot()
    repos = SetRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project,
        bot=bot
    )
    return repos


def get_map():
    return Map(_abspath("./test.map"))


def get_map_repository():
    login_user = get_login_user()
    project = get_project()
    bot = get_bot()
    repos = MapRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project,
        bot=bot
    )
    return repos


def get_property():
    return Property(_abspath("./test.property"))


def get_property_repository():
    login_user = get_login_user()
    project = get_project()
    bot = get_bot()
    repos = PropertyRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project,
        bot=bot
    )
    return repos


def get_config():
    return Config(_abspath("./test.config"))


def get_config_repository():
    login_user = get_login_user()
    project = get_project()
    bot = get_bot()
    repos = ConfigRepository(
        endpoint=MANAGEMENT_ENDPOINT,
        user=login_user,
        project=project,
        bot=bot
    )
    return repos


class UserRepositoryTest(unittest.TestCase):
    def test_login(self):
        login_user = get_login_user()
        self.assertTrue(login_user.authorized)


class ProjectRepositoryTest(unittest.TestCase):
    def test_get(self):
        repos = get_project_repository()
        # 次の呼び出しが例外を出さなければ status_code が 200 番台であることを意味する
        project = get_project()
        project_ = repos.get(project=project)
        self.assertEqual(project_.name, project.name)

    def test_get_all(self):
        repos = get_project_repository()
        # 次の呼び出しが例外を出さなければ status_code が 200 番台であることを意味する
        projects = repos.get_all()
        self.assertTrue(len(projects) >= 0)


class BotRepositoryTest(unittest.TestCase):
    def test_get_all(self):
        repos = get_bot_repository()
        # 次の呼び出しが例外を出さなければ status_code が 200 番台であることを意味する
        bots = repos.get_all()
        self.assertTrue(len(bots) >= 0)

    def test_get(self):
        repos = get_bot_repository()
        bot = get_bot()
        with BotInitializer():
            # 次の呼び出しが例外を出さなければ status_code が 200 番台であることを意味する
            bot_ = repos.get(bot=bot)
            self.assertEqual(bot.id_, bot_.id_)

    def test_add_remove(self):
        repos = get_bot_repository()
        # 次の呼び出しが例外を出さなければ status_code が 200 番台であることを意味する
        bot = get_bot()
        try:
            repos.remove(bot=bot)
        except StatusCodeException:
            pass
        repos.add(bot=bot)
        repos.update(bot=bot)
        repos.remove(bot=bot)

    def test_compile_transfer(self):
        # AIMLが存在しないとボットのコンパイルは404を返すので、AIMLを追加してからテストする
        with BotInitializer():
            bot = get_bot()
            bot_repos = get_bot_repository()
            aiml = get_aiml()
            aiml_repos = get_aiml_repository()

            aiml_repos.upsert(aiml=aiml)
            bot_repos.compile(bot=bot)
            bot_repos.compile_status(bot=bot)
            bot_repos.transfer(bot=bot)
            bot_repos.transfer_status(bot=bot)


class AIMLRepositoryTest(unittest.TestCase):
    def test_upsert(self):
        with BotInitializer():
            repos = get_aiml_repository()
            aiml = get_aiml()
            repos.upsert(aiml=aiml)


class SetRepositoryTest(unittest.TestCase):
    def test_upsert(self):
        with BotInitializer():
            repos = get_set_repository()
            set = get_set()
            repos.upsert(set=set)


class MapRepositoryTest(unittest.TestCase):
    def test_upsert(self):
        with BotInitializer():
            repos = get_map_repository()
            map = get_map()
            repos.upsert(map=map)


class PropertyRepositoryTest(unittest.TestCase):
    def test_upsert(self):
        with BotInitializer():
            repos = get_property_repository()
            property = get_property()
            repos.upsert(property=property)


class ConfigRepositoryTest(unittest.TestCase):
    def test_upsert(self):
        with BotInitializer():
            repos = get_config_repository()
            config = get_config()
            repos.upsert(config=config)


class ApplicationRepositoryTest(unittest.TestCase):
    def test_register(self):
        with BotInitializer():
            repos = ApplicationRepository(
                endpoint=REGISTRATION_ENDPOINT
            )
            app = repos.register(bot=get_bot())
            self.assertTrue(app.app_id)

    def test_register_with_app_id(self):
        with BotInitializer():
            repos = ApplicationRepository(
                endpoint=REGISTRATION_ENDPOINT
            )
            app = repos.register(
                bot=get_bot(),
                app_id="test_app_id"
            )
            self.assertEqual(app.app_id, "test_app_id")


class DialogueRepositoryTest(unittest.TestCase):
    def test_dialogue(self):
        with BotInitializer():
            # Botの準備
            bot = get_bot()
            bot_repos = get_bot_repository()
            aiml = get_aiml()
            aiml_repos = get_aiml_repository()
            aiml_repos.upsert(aiml=aiml)
            bot_repos.compile(bot=bot)
            bot_repos.transfer(bot=bot)

            # 対話のテスト
            app_repos = ApplicationRepository(
                endpoint=REGISTRATION_ENDPOINT
            )
            app = app_repos.register(bot=bot)

            dial_repos = DialogueRepository(
                endpoint=DIALOGUE_ENDPOINT
            )
            request = Request(
                application=app,
                voice_text="ハロー"
            )
            res = dial_repos.dialogue(request)
            self.assertEqual(
                res["systemText"]["expression"],
                "ワールド"
            )


class UtilTest(unittest.TestCase):
    def test_assert_status_code_eq(self):
        expected_code = 200
        actual_code = 200
        assert_status_code(expected_code, actual_code)

    def test_assert_status_code_neq(self):
        expected_code = 200
        actual_code = 404
        with self.assertRaises(StatusCodeException):
            assert_status_code(expected_code, actual_code)
