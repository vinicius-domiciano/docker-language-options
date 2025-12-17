
import asyncio
from typing import override
from sources.app.use_cases.configure_project import ConfigureProjectInputPort, ConfigureProjectOutputPort
from sources.controller.command_execute_controller import CommandExecuteController
from sources.controller.input_confirmation_controller import RequestInputConfirmationControllerCallable, ResponseInputConfirmationControllerCallable
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.infra.dependecy_injection.di import get as get_di
from sources.services.event_listener import EventListener


class ConfigureProjectController(CommandExecuteController):
    
    @override
    def execute(self):
        get_di(ConfigureProjectInputPort).execute(output_port=_ConfigureProjectPresenter())

class _ConfigureProjectPresenter(ConfigureProjectOutputPort):

    @override
    def on_success(self):
        get_di(EventListener).emit(ShowMessageLogListenerCallable("Finalizando processo!"))

    def __register_listener__(self):
        get_di(EventListener).add_listener(
            cls=ResponseInputConfirmationControllerCallable,
            listener=self._on_result
        )

    @override
    async def can_continue(self):
        self.__register_listener__()
        
        self.future = asyncio.Future()

        get_di(EventListener).emit(RequestInputConfirmationControllerCallable(
            message="\n\n"
                "Confirmação!"
                "\nDeseja realmente continuar?\nCaso ja estiver com algum alias configurado ele será resetado"
                "\n(Digite 'S' para confirmar. Qualquer outra tecla será interpretada como 'NÃO'.)"
                "\n\nResposta:\t"
        ))

        return await self.future

    def _on_result(self, callable: ResponseInputConfirmationControllerCallable):
        if self.future and not self.future.done():
            self.future.set_result(callable.response)