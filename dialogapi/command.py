"""CLIコマンドに対応する関数を定義するモジュール"""

import sys
import time


class ProgressBar:
    """進捗表示するクラス。

    With文で利用する
    """
    def __init__(self, text):
        self._text = text

    def update(self):
        print(".", end="", file=sys.stderr)

    def __enter__(self):
        print("{} ...".format(self._text), end="", file=sys.stderr)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # 例外を送出して with ブロックを抜ける場合は done を表示しない
        exit_text = ""
        if not exc_type:
            exit_text = " done"
        print(exit_text, file=sys.stderr)


# Project commands
def project_list(project_repository):
    print("id   name")
    for project in project_repository.get_all():
        print("{:<4d} {}".format(project.id_, project.name))


# Bot commands
def bot_list(bot_repository):
    print("id   sraix   language")
    for bot in bot_repository.get_all():
        print("{:<4} {:<6} {}".format(bot.id_, bot.sraix, bot.language))


def bot_setup(
    bot_repository, aiml_repository, set_repository,
    map_repository, config_repository, property_repository,
    bot, aimls, sets, maps, configs, properties
):
    # 設定内容
    # - ボット追加
    #   - 存在すれば、値を更新する
    # - AIMLのアップロード
    # - SETSのアップロード
    # - MAPSのアップロード
    # - BotConfigの設定
    # - BotPropertyの設定
    #   - 存在すれば、値を更新する
    # - Botのコンパイル
    # - Botの転送
    _bot_upsert(bot_repository, bot)
    aiml_upsert(aiml_repository, aimls)
    set_upsert(set_repository, sets)
    map_upsert(map_repository, maps)
    config_upsert(config_repository, configs)
    property_upsert(property_repository, properties)
    bot_compile(bot_repository, bot)
    bot_transfer(bot_repository, bot)


def bot_add(bot_repository, bot):
    with ProgressBar("Adding bot {}".format(bot.id_)):
        bot_repository.add(bot=bot)


def bot_remove(bot_repository, bot):
    with ProgressBar("Removing bot {}".format(bot.id_)):
        bot_repository.remove(bot=bot)


def _bot_upsert(bot_repository, bot):
    try:
        bot_add(bot_repository, bot)
    except Exception:
        print(
            "-> Bot seems to exist. Updating instead.\n->",
            file=sys.stderr,
            end=" "
        )
        bot_update(bot_repository, bot)


def bot_update(bot_repository, bot):
    with ProgressBar("Updating bot {}".format(bot.id_)):
        bot_repository.update(bot=bot)


def bot_compile(bot_repository, bot):
    with ProgressBar("Compiling bot {}".format(bot.id_)) as pg:
        bot_repository.compile(bot=bot)
        # コンパイルが完了するまで待機する処理
        while True:
            completed = bot_repository.compile_status(bot=bot)
            if completed:
                break
            pg.update()
            time.sleep(1)


def bot_transfer(bot_repository, bot):
    with ProgressBar("Transfering: bot {}".format(bot.id_)) as pg:
        bot_repository.transfer(bot=bot)
        # 転送が完了するまで待機する処理
        while True:
            completed = bot_repository.transfer_status(bot=bot)
            if completed:
                break
            pg.update()
            time.sleep(1)


def bot_test(
    application_repository, dialogue_repository,
    bot, tests
):
    """
    Returns:
        (bool) テストが成功した場合は True を、そうでない場合は False を返す
    """
    test_results = []

    print("Testing bot {}".format(bot.id_))
    for task_manager in tests:
        # app_id登録を行う
        res = task_manager.execute_tasks(
            bot=bot,
            application_repository=application_repository,
            dialogue_repository=dialogue_repository
        )
        test_results.append(res)

    return all(test_results)


def aiml_upsert(aiml_repository, aimls):
    for aiml in aimls:
        with ProgressBar("Uploading AIML {}".format(aiml.filename)):
            aiml_repository.upsert(aiml=aiml)


def set_upsert(set_repository, sets):
    for set_ in sets:
        with ProgressBar("Uploading Set {}".format(set_.filename)):
            set_repository.upsert(set=set_)


def map_upsert(map_repository, maps):
    for map_ in maps:
        with ProgressBar("Uploading Map {}".format(map_.filename)):
            map_repository.upsert(map=map_)


def config_upsert(config_repository, configs):
    for config in configs:
        with ProgressBar("Uploading Config {}".format(config.filename)):
            config_repository.upsert(config=config)


def property_upsert(property_repository, properties):
    for property in properties:
        with ProgressBar("Uploading Property {}".format(property.filename)):
            property_repository.upsert(property=property)
