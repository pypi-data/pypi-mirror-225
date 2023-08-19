import abc

from helm_mkdocs.model import YamlItem

class Generator(abc.ABC):

    def __init__(self, settings):
        self.settings = settings

    @abc.abstractmethod
    def generate_page(self, item: YamlItem) -> str:
        pass
