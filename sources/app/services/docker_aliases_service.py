from abc import ABC, abstractmethod


class DockerAliasesService(ABC):
    def __init__(self): pass

    @abstractmethod
    def update_aliases(self, image_name: str, command: str): pass

    @abstractmethod
    def save_aliases(self): pass

    @abstractmethod
    def contains_alias(self, image_name, alias) -> bool: pass
