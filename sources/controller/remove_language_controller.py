
import asyncio
from typing import override
from sources.app.use_cases.remove_language import RemoveLanguageInputPort, RemoveLanguageOutputPort
from sources.controller.command_execute_controller import CommandExecuteController
from sources.controller.input_confirmation_controller import RequestInputConfirmationControllerCallable, ResponseInputConfirmationControllerCallable
from sources.infra.dependecy_injection.di import get as get_di
from sources.services.event_listener import EventListener


class RemoveLanguageController(CommandExecuteController):
    def __init__(self, language_name: str):
        self.language_name = language_name

    @override
    def execute(self):
        get_di(RemoveLanguageInputPort).execute(
            language=self.language_name,
            output_port=_RemoveLanguagePresenter()
        )

class _RemoveLanguagePresenter(RemoveLanguageOutputPort):
    def __init__(self):
        self.future: asyncio.Future = None

    def __register_listener__(self):
        get_di(EventListener).add_listener(
            cls=ResponseInputConfirmationControllerCallable,
            listener=self._on_result
        )

    @override
    async def can_remove_language_with_aliases(self):
        self.__register_listener__()
        
        self.future = asyncio.Future()

        get_di(EventListener).emit(RequestInputConfirmationControllerCallable(
            message="\n\n"
                "A linguagem selecionada possui uma versão que está sendo utilizada por um alias.\n"
                "Deseja realmente removê-la?"
                "\n(Digite 'S' para confirmar. Qualquer outra tecla será interpretada como 'NÃO'.)"
                "\n\nResposta:\t"
        ))

        return await self.future

    def _on_result(self, callable: ResponseInputConfirmationControllerCallable):
        if self.future and not self.future.done():
            self.future.set_result(callable.response)