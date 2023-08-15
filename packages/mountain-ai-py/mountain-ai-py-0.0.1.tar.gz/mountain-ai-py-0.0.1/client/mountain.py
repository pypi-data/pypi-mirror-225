from abc import ABC, abstractmethod
from team import Team


class Mountain(ABC):
    # 模式，local表示只从本地目录加载数据集，remote表示从远程读取数据集元信息并加载数据
    mode = 'local'

    @abstractmethod
    def team(self, team_name: str) -> Team:
        pass


class MountainImpl(Mountain):

    def team(self, team_name: str) -> Team:
        Team()