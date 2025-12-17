
from abc import ABC, abstractmethod


class DockerProjectConfigurerService(ABC):

    @abstractmethod
    def generate_alias(self): pass

    @abstractmethod
    def run_configurer(self): pass