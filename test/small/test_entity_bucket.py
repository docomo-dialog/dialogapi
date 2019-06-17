import unittest
from dialogapi.entity import Project
from dialogapi.entity import Bot
from dialogapi.entity import AIML
from dialogapi.entity import Set
from dialogapi.entity import Map
from dialogapi.entity import Property
from dialogapi.entity import Config
from dialogapi.entity_bucket import EntityBucket
from dialogapi.entity_bucket import ProjectConfig
from dialogapi.entity_bucket import BotConfig
from dialogapi.test.config import Parser as TestParser


class EntityBucketTest(unittest.TestCase):
    def bulid_bucket(self):
        project_name = "test_project"
        project = Project(name="TEST")

        bot_name = "test_bot"
        bot = Bot(id_="TEST_Bot")
        aimls = [AIML("test.aiml")]
        sets = [Set("test.set")]
        maps = [Map("test.map")]
        properties = [Property("test.property")]
        configs = [Config("test.config")]
        tests = [TestParser()]

        bot_config = BotConfig(
            name=bot_name, bot=bot, aimls=aimls, sets=sets,
            maps=maps, properties=properties, configs=configs,
            tests=tests
        )
        project_config = ProjectConfig(
            name=project_name,
            project=project,
            bot_config_map={bot_name: bot_config}
        )
        project_map = EntityBucket({project_name: project_config})

        return project_map

    def test_get_projects(self):
        bucket = self.bulid_bucket()
        projects = bucket.get_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "TEST")

    def test_get_bots(self):
        bucket = self.bulid_bucket()
        bots = bucket.get_bots(project="test_project")
        self.assertEqual(len(bots), 1)
        self.assertEqual(bots[0].id_, "TEST_Bot")

    def _test_bot_related_entity(self, filename, action):
        bucket = self.bulid_bucket()
        aimls = getattr(bucket, action)(project="test_project", bot="test_bot")
        self.assertEqual(len(aimls), 1)
        self.assertEqual(aimls[0].filename, filename)

    def test_get_aimls(self):
        self._test_bot_related_entity("test.aiml", "get_aimls")

    def test_get_sets(self):
        self._test_bot_related_entity("test.set", "get_sets")

    def test_get_maps(self):
        self._test_bot_related_entity("test.map", "get_maps")

    def test_get_properties(self):
        self._test_bot_related_entity("test.property", "get_properties")

    def test_get_configs(self):
        self._test_bot_related_entity("test.config", "get_configs")

    def test_get_tests(self):
        bucket = self.bulid_bucket()
        tests = bucket.get_tests(project="test_project", bot="test_bot")
        self.assertEqual(len(tests), 1)
