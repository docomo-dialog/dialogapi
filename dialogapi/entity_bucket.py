class EntityBucket:
    """EntityBucketインターフェースを実装するクラス"""
    def __init__(self, project_map):
        """
        Args:
            project_map (Dict[str][ProjectConfig])
        """
        self._project_map = project_map

    def get_projects(self):
        return [
            pconfig.project
            for pconfig in self._project_map.values()
        ]

    def get_project(self, project):
        return self._project_map[project].project

    def get_bots(self, project):
        return [
            bconfig.bot for bconfig in
            self._project_map[project].bot_config_map.values()
        ]

    def get_bot(self, project, bot):
        return self._project_map[project].bot_config_map[bot].bot

    def get_aimls(self, project, bot):
        return self._project_map[project].bot_config_map[bot].aimls

    def get_sets(self, project, bot):
        return self._project_map[project].bot_config_map[bot].sets

    def get_maps(self, project, bot):
        return self._project_map[project].bot_config_map[bot].maps

    def get_configs(self, project, bot):
        return self._project_map[project].bot_config_map[bot].configs

    def get_properties(self, project, bot):
        return self._project_map[project].bot_config_map[bot].properties

    def get_tests(self, project, bot):
        return self._project_map[project].bot_config_map[bot].tests

    def iter_projects(self):
        return [
            (name, pconfig.project) for name, pconfig
            in self._project_map.items()
        ]

    def iter_bots(self, project):
        return [
            (name, bconfig.bot) for name, bconfig in
            self._project_map[project].bot_config_map.items()
        ]


class ProjectConfig:
    """プロジェクト情報を保持するプロジェクト管理オブジェクト"""
    def __init__(self, name, project, bot_config_map):
        """
        Args:
            name (str): プロジェクト名
            server (Server): プロジェクト管理オブジェクト
            bot_config_map (Dict[str][Bot]):
                ボット名とボット管理オブジェクトを対応させる辞書
        """
        self.name = name
        self.project = project
        self.bot_config_map = bot_config_map


class BotConfig:
    """ボット情報を保持するボット管理オブジェクト"""
    def __init__(self, name, bot, aimls, sets,
                 maps, properties, configs, tests):
        """
        Args:
            name (str): ボット名
            bot (Bot): ボット管理オブジェクト
            aimls (List[AIML]): このボットの管理対象となるAIML管理オブジェクトのリスト
            sets (List[Set]): このbotの管理対象となる Set 管理オブジェクトのリスト
            maps (List[Map]): このbotの管理対象となる Map 管理オブジェクトのリスト
            properties (List[Property]):
                ボットプロパティを表す Property 管理オブジェクトのリスト
            configs (List[Config]):
                ボットコンフィグを表す Config 管理オブジェクトのリスト
            tests (List[Test]): このbotのテストオブジェクトのリスト
        """
        self.name = name
        self.bot = bot
        self.aimls = aimls
        self.sets = sets
        self.maps = maps
        self.properties = properties
        self.configs = configs
        self.tests = tests
