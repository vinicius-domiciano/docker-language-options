from abc import ABC, abstractmethod
from sources.services.event_listener import EventListener
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService

class AddNewLanguageInputPort(ABC):
    
    @abstractmethod
    def execute(self, name:str) -> None: pass

class AddNewLanguage(AddNewLanguageInputPort):
    def __init__(self, listener: EventListener, docker_options_service: DockerOptionsConfigurerService):
        self.listener = listener
        self.docker_options_service = docker_options_service

    def execute(self, name):
        if not name:
            self.listener.emit(ShowMessageLogListenerCallable("O nome da linguagem deve ser informado!"))
            return
        
        if self.docker_options_service.verify_language_exists(name):
            self.listener.emit(ShowMessageLogListenerCallable("A linguagem informada já existe!"))
            return
        
        self.docker_options_service.add_new_language(name)
        self.listener.emit(ShowMessageLogListenerCallable(f"Linguagem [{name}] inserida com sucesso"))