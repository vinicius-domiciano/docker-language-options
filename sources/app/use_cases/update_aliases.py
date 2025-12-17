
from abc import ABC, abstractmethod

from sources.app.services.docker_aliases_service import DockerAliasesService
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.services.event_listener import EventListener


class UpdateAliasesOutputPort(ABC):

    @abstractmethod
    def on_success(self): pass


class UpdateAliasesInputPort(ABC):

    @abstractmethod
    def execute(
            self,
            image_name: str,
            aliases: list[str],
            output_port: UpdateAliasesOutputPort
    ): pass

class UpdateAliasesImpl(UpdateAliasesInputPort):
    def __init__(self, listener: EventListener, service: DockerAliasesService):
        self.listener = listener
        self.service = service

    def execute(self, image_name, aliases, output_port):
        self.listener.emit(ShowMessageLogListenerCallable("Atualizando aliases"))

        for alias in aliases:
            self.service.update_aliases(image_name=image_name, command=alias)

        self.service.save_aliases()

        output_port.on_success()