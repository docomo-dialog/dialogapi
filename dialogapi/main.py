import sys
import click
import dialogapi.command as command
from dialogapi.config_parser import build_entity_bucket
from dialogapi.repository_factory import RepositoryFactory

# エラー時のトレースバック出力を制御する
sys.tracebacklimit = 0


def build_repository_factory(server, auth=True):
    return RepositoryFactory(server=server, auth=auth)


@click.group()
def cmd():
    """NLU Management API クライアントツール"""
    pass


# プロジェクト関連 #
@click.group()
def project():
    """プロジェクト管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
def project_list(config, server):
    """プロジェクト一覧を表示する"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    command.project_list(
        project_repository=repos_factory.create_project_repository()
    )


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
def project_setup(config, server, project):
    """プロジェクトのボット作成・設定を行う"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    for bot_name, _ in entity_bucket.iter_bots(project=project):
        _bot_setup(entity_bucket, repos_factory, project, bot_name)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="server", type=str, required=True)
def project_reset(config, server, project):
    """ボットを全て削除してプロジェクトを新規の状態にする"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    project_ = entity_bucket.get_project(project=project)
    bot_repository = repos_factory.create_bot_repository(project=project_)

    for bot in bot_repository.get_all():
        command.bot_remove(bot_repository=bot_repository, bot=bot)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
def project_test(config, server, project):
    """プロジェクトの全てのボットをテストする"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_, auth=False)
    results = []
    for bot_name, _ in entity_bucket.iter_bots(project=project):
        res = _bot_test(entity_bucket, repos_factory, project, bot_name)
        results.append(res)
    _judge_test(results)


project.add_command(project_list, name="list")
project.add_command(project_setup, name="setup")
project.add_command(project_reset, name="reset")
project.add_command(project_test, name="test")
cmd.add_command(project)


# ボット関連 #
@click.group()
def bot():
    """ボット管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="server", type=str, required=True)
def bot_list(config, server, project):
    """ボット一覧を表示する"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    project = entity_bucket.get_project(project=project)
    command.bot_list(
        bot_repository=repos_factory.create_bot_repository(project=project)
    )


def _bot_setup(entity_bucket, repos_factory, project, bot):
    repos = repos_factory  # rename repos_factory for shorthand
    project_ = entity_bucket.get_project(project=project)
    bot_ = entity_bucket.get_bot(project=project, bot=bot)
    command.bot_setup(
        bot_repository=repos.create_bot_repository(project=project_),
        aiml_repository=repos.create_aiml_repository(
            project=project_, bot=bot_
        ),
        set_repository=repos.create_set_repository(project=project_, bot=bot_),
        map_repository=repos.create_map_repository(project=project_, bot=bot_),
        config_repository=repos.create_config_repository(
            project=project_, bot=bot_
        ),
        property_repository=repos.create_property_repository(
            project=project_, bot=bot_
        ),
        bot=entity_bucket.get_bot(project=project, bot=bot),
        aimls=entity_bucket.get_aimls(project=project, bot=bot),
        sets=entity_bucket.get_sets(project=project, bot=bot),
        maps=entity_bucket.get_maps(project=project, bot=bot),
        configs=entity_bucket.get_configs(project=project, bot=bot),
        properties=entity_bucket.get_properties(project=project, bot=bot)
    )


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str, required=True)
def bot_setup(config, server, project, bot):
    """ボットを追加・設定する"""
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    _bot_setup(entity_bucket, repos_factory, project, bot)


def _bot_helper(action, config, server, project, bot):
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    project_ = entity_bucket.get_project(project=project)
    getattr(command, action)(
        bot_repository=repos_factory.create_bot_repository(project=project_),
        bot=entity_bucket.get_bot(project=project, bot=bot)
    )


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str, required=True)
def bot_add(config, server, project, bot):
    """ボットを追加する"""
    _bot_helper("bot_add", config, server, project, bot)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def bot_remove(config, server, project, bot):
    """ボットを削除する"""
    _bot_helper("bot_remove", config, server, project, bot)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def bot_update(config, server, project, bot):
    """ボットを更新する"""
    _bot_helper("bot_update", config, server, project, bot)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def bot_compile(config, server, project, bot):
    """ボットをコンパイルする"""
    _bot_helper("bot_compile", config, server, project, bot)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def bot_transfer(config, server, project, bot):
    """ボットを転送する"""
    _bot_helper("bot_transfer", config, server, project, bot)


def _bot_test(entity_bucket, repos_factory, project, bot):
    """ボットをテストする"""
    tests = entity_bucket.get_tests(project=project, bot=bot)
    bot_ = entity_bucket.get_bot(project=project, bot=bot)

    return command.bot_test(
        repos_factory.create_application_repository(),
        repos_factory.create_dialogue_repository(),
        bot_, tests
    )


def _judge_test(results):
    if not all(results):
        print("Test Failed", file=sys.stderr)
        sys.exit(1)


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def bot_test(config, server, project, bot):
    """ボットをテストする"""
    server_, entity_bucket = build_entity_bucket(config, server)
    # テスト時は Project オブジェクトに project_id を設定する必要がないため、
    # Management API の認証は行わない
    repos_factory = build_repository_factory(server_, auth=False)
    test_result = _bot_test(entity_bucket, repos_factory, project, bot)
    _judge_test([test_result])


bot.add_command(bot_list,     name="list")
bot.add_command(bot_setup,    name="setup")
bot.add_command(bot_add,      name="add")
bot.add_command(bot_remove,   name="remove")
bot.add_command(bot_update,   name="update")
bot.add_command(bot_compile,  name="compile")
bot.add_command(bot_transfer, name="transfer")
bot.add_command(bot_test,     name="test")
cmd.add_command(bot)


def _bot_entity_helper(action_set, config, server, project, bot):
    server_, entity_bucket = build_entity_bucket(config, server)
    repos_factory = build_repository_factory(server_)
    project_ = entity_bucket.get_project(project=project)
    bot_ = entity_bucket.get_bot(project=project, bot=bot)

    repos = getattr(repos_factory, action_set[0])(project=project_, bot=bot_)
    items = getattr(entity_bucket, action_set[1])(project=project, bot=bot)
    getattr(command, action_set[2])(repos, items)


# AIML関連 #
@click.group()
def aiml():
    """AIML管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str, required=True)
def aiml_upsert(config, server, project, bot):
    """AIMLを追加、更新する"""
    _bot_entity_helper(
        ("create_aiml_repository", "get_aimls", "aiml_upsert"),
        config, server, project, bot
    )


aiml.add_command(aiml_upsert, name="upsert")
cmd.add_command(aiml)


# SETS関連 #
@click.group()
def set_():
    """SET管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def set_upsert(config, server, project, bot):
    """SETを追加、更新する"""
    _bot_entity_helper(
        ("create_set_repository", "get_sets", "set_upsert"),
        config, server, project, bot
    )


set_.add_command(set_upsert, name="upsert")
cmd.add_command(set_, name="set")


# MAPS関連 #
@click.group()
def map_():
    """MAP管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def map_upsert(config, server, project, bot):
    """MAPを追加、更新する"""
    _bot_entity_helper(
        ("create_map_repository", "get_maps", "map_upsert"),
        config, server, project, bot
    )


map_.add_command(map_upsert, name="upsert")
cmd.add_command(map_, name="map")


# BOT PROPERTY関連 #
@click.group()
def property_():
    """BotProperty管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def property_upsert(config, server, project, bot):
    """BotPropertyを追加、更新する"""
    _bot_entity_helper(
        ("create_property_repository", "get_properties", "property_upsert"),
        config, server, project, bot
    )


property_.add_command(property_upsert, name="upsert")
cmd.add_command(property_, name="property")


# BotConfig関連 #
@click.group()
def config_():
    """BotConfig管理コマンド"""
    pass


@click.command()
@click.option('--config', help='config file', type=str, required=True)
@click.option('--server', help="server", type=str, required=True)
@click.option('--project', help="project", type=str, required=True)
@click.option('--bot', help="bot", type=str)
def config_upsert(config, server, project, bot):
    """BotConfigを追加、更新する"""
    _bot_entity_helper(
        ("create_config_repository", "get_configs", "config_upsert"),
        config, server, project, bot
    )


config_.add_command(config_upsert, name="upsert")
cmd.add_command(config_, name="config")


if __name__ == "__main__":
    cmd()
