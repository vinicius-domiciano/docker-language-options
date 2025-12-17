
from abc import ABC,abstractmethod
from typing import override

from sources.app.services.docker_commands_service import DockerCommandsService


class DownloadImageOutputPort(ABC):

    @abstractmethod
    def on_success(self, image_name:str): pass

class DownloadImageInputPort(ABC):

    @abstractmethod
    def execute(self, image_name:str, output_port: DownloadImageOutputPort): pass

class DownloadImageImpl(DownloadImageInputPort):
    def __init__(self, commands_service: DockerCommandsService):
        self.commands_service = commands_service

    @override
    def execute(self, image_name, output_port):
        self.commands_service.pull_image(image_name)
        output_port.on_success(image_name)