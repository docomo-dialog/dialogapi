from dialogapi.repository import ProjectRepository
from dialogapi.repository import UserRepository
from dialogapi.repository import BotRepository
from dialogapi.repository import AIMLRepository
from dialogapi.repository import ApplicationRepository
from dialogapi.repository import DialogueRepository
from dialogapi.repository import SetRepository
from dialogapi.repository import MapRepository
from dialogapi.repository import ConfigRepository
from dialogapi.repository import PropertyRepository


class RepositoryFactory:
    """リポジトリを生成するクラス

    Abstract factrory パターンにしたがって、RepositoryFactory を実装する
    """
    def __init__(self, server, auth=True):
        self._server = server
        self._user = server.user

        if auth:
            self._auth()

    def _auth(self):
        user_repository = UserRepository(
            endpoint=self._server.management_endpoint
        )
        user_repository.login(user=self._user)

    def create_project_repository(self):
        repos = ProjectRepository(
            endpoint=self._server._management_endpoint,
            user=self._user,
        )
        return repos

    def create_bot_repository(self, project):
        project_ = self.create_project_repository().get(project=project)
        bot_repository = BotRepository(
            endpoint=self._server.management_endpoint,
            user=self._user,
            project=project_,
        )
        return bot_repository

    def create_aiml_repository(self, project, bot):
        return self._bot_repos(AIMLRepository, project, bot)

    def create_set_repository(self, project, bot):
        return self._bot_repos(SetRepository, project, bot)

    def create_map_repository(self, project, bot):
        return self._bot_repos(MapRepository, project, bot)

    def create_property_repository(self, project, bot):
        return self._bot_repos(PropertyRepository, project, bot)

    def create_config_repository(self, project, bot):
        return self._bot_repos(ConfigRepository, project, bot)

    def create_application_repository(self):
        return ApplicationRepository(
            endpoint=self._server.registration_endpoint
        )

    def create_dialogue_repository(self):
        return DialogueRepository(endpoint=self._server.dialogue_endpoint)

    def _bot_repos(self, cls, project, bot):
        # project id を取得するために一度サーバに問い合わせる
        endpoint = self._server._management_endpoint
        project = self.create_project_repository().get(project=project)
        args = (endpoint, self._user, project, bot)
        repository = cls(*args)
        return repository
