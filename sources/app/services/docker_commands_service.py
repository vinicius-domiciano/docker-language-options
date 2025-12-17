from abc import ABC, abstractmethod

class DockerCommandsService(ABC):

    @abstractmethod
    def build_docker_file(self, image_name: str): pass

    @abstractmethod
    def pull_image(self, image_name: str): pass