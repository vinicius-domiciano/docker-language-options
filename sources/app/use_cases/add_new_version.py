from abc import ABC, abstractmethod
import uuid

from sources.app.models.argument import ArgumentParams
from sources.services.event_listener import EventListener
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService

class AddNewVersionOutputPort(ABC):

    @abstractmethod
    def on_success(self, image_name:str): pass

    @abstractmethod
    def on_failure(self, message: str): pass

class AddNewVersionInputPort(ABC):
    
    @abstractmethod
    def execute(self, arguments: ArgumentParams, output_port: AddNewVersionOutputPort) -> None: pass


class AddNewVersion(AddNewVersionInputPort):
    def __init__(self, listener: EventListener, docker_options_service: DockerOptionsConfigurerService):
        self.listener = listener
        self.docker_options_service = docker_options_service
        
    def execute(self, arguments, output_port):
        language = arguments.language
        version = arguments.version

        if not language or not version:
            output_port.on_failure("nome e a versão devem ser preenchidos!")
            return
    
        if not self.docker_options_service.verify_language_exists(language):
            output_port.on_failure(f"A linguagem [{language}], não foi encontrada")
            return
    
        options: dict = self.docker_options_service.get_languages_properties(language)
        if options.get(version):
            output_port.on_failure(f"Versão informada já existe!!")
            return
        
        container_name = f'docker-options_{str(uuid.uuid4())}'
        image_name = container_name
        use_dockerfile = True
        environments: list[str] = []

        if arguments.use_image: 
            image_name = arguments.image_name
            use_dockerfile = False
        else:
            environments.extend(arguments.envs)

        version_opt: dict = {version: {
            'image_name': image_name,
            'name': container_name,
            'use_dockerfile': use_dockerfile,
            'environments': environments,
            'alias': arguments.aliases
        }}

        self.docker_options_service.add_new_version(language, version_opt)
        self.listener.emit(ShowMessageLogListenerCallable(message="Versão adicionada com sucesso"))
        output_port.on_success(image_name)
