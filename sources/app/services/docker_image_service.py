from abc import ABC, abstractmethod
from sources.app.models.image_file import ImageFile

class DockerImageService(ABC):

    @abstractmethod
    def create_image_file(self, request: ImageFile): pass

    @abstractmethod
    def create_volume_name(self, language: str, version: str): pass