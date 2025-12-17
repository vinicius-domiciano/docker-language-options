from abc import ABC, abstractmethod

from sources.app.services.docker_commands_service import DockerCommandsService
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.services.event_listener import EventListener

class BuildDockerFileOutputPort(ABC):

    @abstractmethod
    def on_success(self, image_name: str): pass


class BuildDockerFileInputPort(ABC):

    @abstractmethod
    def execute(self, image_name: str, output_port: BuildDockerFileOutputPort): pass

class BuildDockerFile(BuildDockerFileInputPort):
    def __init__(self, commands_service: DockerCommandsService, listener: EventListener):
        self.commands_service = commands_service
        self.listener = listener

    def execute(self, image_name, output_port):
        self.listener.emit(ShowMessageLogListenerCallable("Iniciando build do dockerfile"))
        self.commands_service.build_docker_file(image_name)

        output_port.on_success(image_name)