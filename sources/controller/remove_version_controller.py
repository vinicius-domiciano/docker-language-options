
import asyncio
from typing import override
from sources.app.use_cases.remove_version import RemoveVersionInputPort, RemoveVersionOutputPort
from sources.controller.command_execute_controller import CommandExecuteController
from sources.controller.input_confirmation_controller import RequestInputConfirmationControllerCallable, ResponseInputConfirmationControllerCallable
from sources.infra.dependecy_injection.di import get as get_di
from sources.services.event_listener import EventListener

class RemoveVersionController(CommandExecuteController):
    def __init__(self, language_name: str, version_name: str):
        self.language_name = language_name
        self.version_name = version_name

    @override
    def execute(self):
        get_di(RemoveVersionInputPort).execute(
            language=self.language_name,
            version_name=self.version_name,
            output_port=_RemoveLanguagePresenter()
        )

class _RemoveLanguagePresenter(RemoveVersionOutputPort):
    def __init__(self):
        self.future: asyncio.Future = None

    def __register_listener__(self):
        get_di(EventListener).add_listener(
            cls=ResponseInputConfirmationControllerCallable,
            listener=self._on_result
        )

    @override
    async def can_remove_version_with_alias(self):
        self.__register_listener__()
        
        self.future = asyncio.Future()

        get_di(EventListener).emit(RequestInputConfirmationControllerCallable(
            message="\n\n"
                "A versão informada está sendo utilizada por um alias.\n"
                "Deseja realmente removê-la?"
                "\n(Digite 'S' para confirmar. Qualquer outra tecla será interpretada como 'NÃO'.)"
                "\n\nResposta:\t"
        ))

        return await self.future

    def _on_result(self, callable: ResponseInputConfirmationControllerCallable):
        if self.future and not self.future.done():
            self.future.set_result(callable.response)