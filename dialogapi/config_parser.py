"""プロジェクト構成ファイルを解析して EntityBucket を生成するモジュール"""


import yaml
from dialogapi.server import Server
from dialogapi.server import Endpoint
from dialogapi.entity import Project
from dialogapi.entity import Bot
from dialogapi.entity import AIML
from dialogapi.entity import Set
from dialogapi.entity import Map
from dialogapi.entity import User
from dialogapi.entity import Property
from dialogapi.entity import Config as BConfig
from dialogapi.entity_bucket import EntityBucket
from dialogapi.entity_bucket import ProjectConfig
from dialogapi.entity_bucket import BotConfig
from dialogapi.test.config import Parser as TestParser
import re
import os


def build_entity_bucket(config, server):
    """プロジェクト構成ファイルからエンティティバケットを構築するファクトリ関数

    Args:
        config (str): ファイル名
        server (str): サーバ名
    Returns:
        (Server, EntityBucket): サーバとエンティティバケットを返す
    """

    server_, entity_bucket = Parser().parse(config, server, context=os.environ)
    return server_, entity_bucket


class Parser:
    """プロジェクト構成ファイルを解析して ResourceBucketを生成するクラス"""
    def parse(self, filename, server, context):
        """プロジェクト構成ファイルを解析する

        Args:
            filename (str): プロジェクト構成ファイル名
            server (str): サーバ名
            context (Dict[str][str]): 設定ファイルのプレースホルダーへの値を保持する辞書

        Returns:
            ResourceBucket: ResourceBucket インターフェースを実装するオブジェクト
        """
        with open(filename) as f:
            content = f.read()
        return self.parse_fd(content, server, context)

    def parse_fd(self, content, server, context):
        yaml_dic = yaml.load(self._replace_var(content, context))

        server_map = _ServerParser().parse(yaml_dic["servers"])
        server = server_map[server]
        project_map = _ProjectParser().parse(yaml_dic["projects"])

        return (server, EntityBucket(project_map=project_map))

    def _replace_var(self, content, context):
        """YAMLファイル中の環境変数を置き換える"""
        regex = re.compile(r'\${([a-zA-Z_]+[a-zA-Z0-9_]*)}')
        while True:
            match = regex.search(content)
            if not match:
                break
            content = content.replace(match.group(0), context[match.group(1)])
        return content


class ParserException(Exception):
    """プロジェクト構成ファイル解析時のエラーを表すクラス"""


def _get(dic, key):
    return dic.get(key)


def _get_default(dic, key, default):
    return dic.get(key, default)


def _validate(key, keys):
    if key not in keys:
        raise ParserException("{} not in {}".format(key, keys))


def _validate_dic(dic, keys):
    for key in dic:
        _validate(key, keys)


class _ServerParser:
    """プロジェクト構成ファイルのサーバセクションを解析するクラス"""
    def _get_endpoint(self, endpoint, name, host, port, protocol):
        if name in endpoint:
            return Endpoint(
                host=host, port=port, protocol=protocol,
                prefix=endpoint[name]["prefix"],
                header=endpoint[name]["header"],
            )
        else:
            return None

    def parse(self, servers):
        server_map = dict()
        for item in servers:
            server_config = _get(item, "config")
            endpoint = _get(server_config, "endpoint")
            host = _get(server_config, "host")
            port = _get(server_config, "port")
            protocol = _get(server_config, "protocol")

            management = self._get_endpoint(
                endpoint, "management",
                host, port, protocol
            )
            registration = self._get_endpoint(
                endpoint, "registration",
                host, port, protocol
            )
            dialogue = self._get_endpoint(
                endpoint, "dialogue",
                host, port, protocol
            )
            user = User(
                name=_get_default(server_config, "user", None),
                password=_get_default(server_config, "password", None)
            )
            server = Server(
                management_endpoint=management,
                registration_endpoint=registration,
                dialogue_endpoint=dialogue,
                user=user,
                ssl_verify=server_config.get("ssl_verify", True)
            )

            name = _get(item, "name")
            server_map[name] = server
        return server_map


class _ProjectParser:
    def parse(self, project_items):
        # server
        projects = []
        for item in project_items:
            name = _get(item, "name")
            project_config = _get(item, "config")
            project = Project(name=_get(project_config, "project_name"))
            bot_config_map = self._parse_bots(_get(item, "bots"))
            project_config = ProjectConfig(name=name,
                                           project=project,
                                           bot_config_map=bot_config_map)
            projects.append(project_config)
        return _build_map(projects)

    def _parse_bots(self, bot_items):
        # server
        bots = []
        for item in bot_items:
            # キーが可能ないずれかにに含まれているかチェックする
            _validate_dic(
                item,
                {"name", "config", "aimls", "sets", "maps",
                 "properties", "configs", "tests"}
            )

            name = _get(item, "name")
            bot_config = _get(item, "config")
            # キーが可能ないずれかにに含まれているかチェックする
            _validate_dic(
                bot_config,
                {"bot_id", "scenario_project_id", "language",
                 "description", "sraix"}
            )

            bot = Bot(
                id_=_get(bot_config, "bot_id"),
                scenario_project_id=_get_default(
                    bot_config,
                    "scenario_project_id",
                    "DSU"
                ),
                language=_get_default(bot_config, "language", "ja-JP"),
                description=_get_default(bot_config, "description", ""),
                sraix=_get_default(bot_config, "sraix", "null")
            )
            aimls = [
                AIML(filename=filename)
                for filename in _get_default(item, "aimls", [])
            ]
            sets = [
                Set(filename=filename)
                for filename in _get_default(item, "sets", [])
            ]
            maps = [
                Map(filename=filename)
                for filename in _get_default(item, "maps", [])
            ]
            properties = [
                Property(filename=filename)
                for filename in _get_default(item, "properties", [])
            ]
            configs = [
                BConfig(filename=filename)
                for filename in _get_default(item, "configs", [])
            ]
            # テスト
            tests = [
                TestParser().parse(filename)
                for filename in _get_default(item, "tests", [])
            ]
            bot_config = BotConfig(
                name=name, bot=bot, aimls=aimls,
                sets=sets, maps=maps,
                properties=properties,
                configs=configs, tests=tests
            )
            bots.append(bot_config)
        return _build_map(bots)


def _build_map(items):
    """name 属性をもつオブジェクトのリストから name をキー、オブジェクトを値とする辞書を構築する

    Args:
        items (List[object]): name を属性を持つオブジェクトのリスト

    Returns:
        Dict[str]object: オブジェクトの name 属性をキーとするオブジェクトを値とした辞書
    """
    dic = dict()
    for item in items:
        if item.name in dic:
            raise Exception("Key duplicated")
        dic[item.name] = item
    return dic
