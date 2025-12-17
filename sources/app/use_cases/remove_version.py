from abc import ABC, abstractmethod
import asyncio
from sources.app.services.docker_aliases_service import DockerAliasesService
from sources.services.event_listener import EventListener
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService

class RemoveVersionOutputPort(ABC):

    @abstractmethod
    async def can_remove_version_with_alias(self): pass

class RemoveVersionInputPort(ABC):
    
    @abstractmethod
    def execute(self, language: str, version_name: str, output_port: RemoveVersionOutputPort):
        pass

class RemoveVersion(RemoveVersionInputPort):
    def __init__(self, listener: EventListener, docker_options_service: DockerOptionsConfigurerService, alias_service: DockerAliasesService):
        self.listener = listener
        self.docker_options_service = docker_options_service
        self.alias_service = alias_service

    def execute(self, language, version_name, output_port):
        if not language or not version_name:
            self.listener.emit(ShowMessageLogListenerCallable("A linguagem e a versão deve ser exibida"))
            return
        
        options: dict = self.docker_options_service.get_languages_properties(language)
        if not options:
            self.listener.emit(ShowMessageLogListenerCallable(message=f"A linguagem [{language}], não foi encontrada"))
            return
        
        version = options.get(version_name) 
        if not version: 
            self.listener.emit(ShowMessageLogListenerCallable(message=f"Versão informada não existe!!"))
            return
        elif self._verify_if_language_versions_have_alias(version):
            can_remove = asyncio.run(output_port.can_remove_version_with_alias())

            if not can_remove:
                self.listener.emit(ShowMessageLogListenerCallable("Finalizando processo..."))
                return       

        self.docker_options_service.remove_version(language, version_name)

    def _verify_if_language_versions_have_alias(self, version: dict):
        for alias in version.get('alias'):
            exist_alias = self.alias_service.contains_alias(version.get('image_name'), alias)
            if exist_alias: return True

        return False