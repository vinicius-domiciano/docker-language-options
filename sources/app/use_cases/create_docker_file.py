from sources.app.models.argument import ArgumentParams
from sources.app.models.image_file import ImageFile
from sources.app.services.docker_image_service import DockerImageService
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from abc import ABC, abstractmethod
from sources.services.event_listener import EventListener

class CreateDockerFileOutputPort(ABC):
    @abstractmethod
    def on_success(self, image_name): pass

class CreateDockerFileInputPort(ABC):

    @abstractmethod
    def execute(self, output_port: CreateDockerFileOutputPort, argument: ArgumentParams): pass

class CreateDockerFile(CreateDockerFileInputPort):
    def __init__(self, listener: EventListener, docker_image_service: DockerImageService):
        self.listener = listener
        self.docker_image_service = docker_image_service

    def execute(self, output_port, argument):
        docker_file_name = "dockerfile.language-up"
        self.listener.emit(ShowMessageLogListenerCallable(f"Criando arquivo {docker_file_name}"))

        docker_file = ImageFile()
        docker_file.image_name = argument.image_name
        docker_file.language_name = argument.language
        docker_file.language_url = argument.url
        docker_file.executable_path = argument.executable_path
        docker_file.required_libs.extend(argument.programs_to_install)
        docker_file.environments.extend(argument.envs)
        docker_file.file_name = docker_file_name

        self.docker_image_service.create_image_file(docker_file)

        output_port.on_success(image_name=docker_file.image_name)