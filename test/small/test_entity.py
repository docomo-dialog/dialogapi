import unittest
import os
from dialogapi.entity import User
from dialogapi.entity import Project
from dialogapi.entity import Bot
from dialogapi.entity import _FileResource
from dialogapi.entity import _KeyValueResource
from dialogapi.entity import Application


class UserTest(unittest.TestCase):
    def test_attribute(self):
        name = "test_user"
        user = User(name=name)
        self.assertEqual(user.name, name)
        self.assertEqual(user.authorized, False)

    def test_user_init_with_access_token(self):
        user = User(name="test_user", access_token="A")
        self.assertEqual(user.authorized, True)

    def test_set_authorized(self):
        user = User(name="test_user")
        self.assertEqual(user.authorized, False)
        user.set_authorized(access_token="A")
        self.assertEqual(user.authorized, True)


class ProjectTest(unittest.TestCase):
    def test_attribute(self):
        id_ = 2
        name = "FAQ"
        organization_id = 2,
        create_date = '2018-11-07 18:02:15.0'
        project = Project(
            id_=id_,
            name=name,
            organization_id=organization_id,
            create_date=create_date
        )

        self.assertEqual(project.id_, id_)
        self.assertEqual(project.name, name)

    def test_attribute_min(self):
        name = "FAQ"
        project = Project(name=name)

        self.assertEqual(project.name, name)
        self.assertEqual(project.id_, None)


class BotTest(unittest.TestCase):
    def test_attribute_min(self):
        bot_id = "TestBot"
        bot = Bot(id_=bot_id)
        self.assertEqual(bot.id_, bot_id)
        self.assertEqual(bot.project, None)
        self.assertEqual(bot.scenario_project_id, "DSU")
        self.assertEqual(bot.language, "ja-JP")
        self.assertEqual(bot.description, "")
        self.assertEqual(bot.sraix, "null")

    def test_attribute(self):
        bot_id = "TestBot"
        project_name = "TestProject"
        scenario_project_id = "TestId"
        language = "en-US"
        description = "テスト"
        sraix = "global"

        bot = Bot(
            id_=bot_id,
            project=Project(name=project_name),
            scenario_project_id=scenario_project_id,
            language=language,
            description=description,
            sraix=sraix
        )
        self.assertEqual(bot.id_, bot_id)
        self.assertEqual(bot.project.name, project_name)
        self.assertEqual(bot.scenario_project_id, scenario_project_id)
        self.assertEqual(bot.language, language)
        self.assertEqual(bot.description, description)
        self.assertEqual(bot.sraix, sraix)


class FileResourceTest(unittest.TestCase):
    def __init__(self):
        filename = "test.aiml"
        resource = _FileResource(filename=filename)
        self.assertEqual(resource.filename, filename)


class KeyValueResourceTest(unittest.TestCase):
    def test_dict(self):
        def abspath(filename):
            return os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                filename
            )

        resource = _KeyValueResource(abspath("test.config"))
        self.assertEqual(
            resource.dict(),
            {'xxx_Url': 'http://test.example.com'}
        )

    def test_dict_no_exist(self):
        resource = _KeyValueResource("test.config.noexist")
        with self.assertRaises(FileNotFoundError):
            resource.dict()


class ApplicationTest(unittest.TestCase):
    def test_constructor(self):
        bot_id = "TestBot"
        app_id = "test_app_id"
        bot = Bot(id_="TestBot")
        app = Application(bot=bot, app_id=app_id)
        self.assertEqual(app.bot.id_, bot_id)
        self.assertEqual(app.app_id, app_id)
