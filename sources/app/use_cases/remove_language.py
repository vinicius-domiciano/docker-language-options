from abc import ABC, abstractmethod
import asyncio
from sources.app.services.docker_aliases_service import DockerAliasesService
from sources.services.event_listener import EventListener
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService

class RemoveLanguageOutputPort(ABC):

    @abstractmethod
    async def can_remove_language_with_aliases(self): bool

class RemoveLanguageInputPort(ABC):
    
    @abstractmethod
    def execute(self, language: str, output_port: RemoveLanguageOutputPort):
        pass

class RemoveLanguage(RemoveLanguageInputPort):
    def __init__(self, listener: EventListener, docker_options_service: DockerOptionsConfigurerService, alias_service: DockerAliasesService):
        self.listener = listener
        self.docker_options_service = docker_options_service
        self.alias_service = alias_service

    def execute(self, language, output_port):
        if not language:
            self.listener.emit(ShowMessageLogListenerCallable("A linguagem deve ser informada"))
            return
        
        if not self.docker_options_service.verify_language_exists(language):
            self.listener.emit(ShowMessageLogListenerCallable(f"A linguagem informada [{language}], não foi encontrada"))
            return
        
        if self._verify_if_language_versions_have_alias(language):
            can_remove = asyncio.run(output_port.can_remove_language_with_aliases())

            if not can_remove:
                self.listener.emit(ShowMessageLogListenerCallable(f"Finalizando o processo..."))
                return
            
        self.docker_options_service.remove_language(language)
        self.listener.emit(ShowMessageLogListenerCallable(f"Linguagem removida com suceeso"))

    def _verify_if_language_versions_have_alias(self, language:str):
        versions = self.docker_options_service.get_languages_properties(language)

        for key in versions.keys():
            version: dict = versions.get(key)
            
            for alias in version.get('alias'):
                exist_alias = self.alias_service.contains_alias(version.get('image_name'), alias)
                if exist_alias: return True

        return False