
import asyncio
from sources.app.use_cases.change_version import ChangeVersionInputPort, ChangeVersionOutputPort
from sources.app.use_cases.update_aliases import UpdateAliasesInputPort, UpdateAliasesOutputPort
from sources.controller.command_execute_controller import CommandExecuteController

from typing import override

from sources.controller.input_confirmation_controller import RequestInputConfirmationControllerCallable, ResponseInputConfirmationControllerCallable
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.infra.dependecy_injection.di import get as di_get
from sources.services.event_listener import EventListener


class ChangeVersionController(CommandExecuteController):

    def __init__(self, language_name: str, version_name: str):
        self.language_name = language_name
        self.version_name = version_name

    @override
    def execute(self):
        di_get(ChangeVersionInputPort).execute(
            version_name=self.version_name, 
            language_name=self.language_name,
            output_port=_ChangeVersionPresenter(self)
        )

    def update_aliases(self, image_name: str, aliases: list[str]): 
        di_get(UpdateAliasesInputPort).execute(
            image_name=image_name, 
            aliases=aliases,
            output_port=_UpdateAliasesPresenter()
        )
        
class _UpdateAliasesPresenter(UpdateAliasesOutputPort):
    
    @override
    def on_success(self):
        di_get(EventListener).emit(ShowMessageLogListenerCallable("\n>> Versão alterada com sucesso! <<\n"))

class _ChangeVersionPresenter(ChangeVersionOutputPort):
    def __init__(self, controller: ChangeVersionController):
        self._controller = controller
        self.future: asyncio.Future = None

    def __register_listener__(self):
        di_get(EventListener).add_listener(
            cls=ResponseInputConfirmationControllerCallable,
            listener=self._on_result
        )

    @override
    def on_success(self, image_name, aliases):
        self._controller.update_aliases(image_name, aliases)

    @override
    def on_error(self, message):
        di_get(EventListener).emit(ShowMessageLogListenerCallable(message))

    @override
    async def can_change_version_from_language(self, version_name, language_name):
        self.__register_listener__()
        self.future = asyncio.Future()

        di_get(EventListener).emit(RequestInputConfirmationControllerCallable(
            f"\n\nTem certeza que deseja mudar a versão da linguagem: {language_name},"
            f" para a versão: {version_name}"
            "\n(Digite 'S' para confirmar. Qualquer outra tecla será interpretada como 'NÃO'.)"
            "\n\nResposta:\t"
        ))

        return await self.future
    
    def _on_result(self, callable: ResponseInputConfirmationControllerCallable):
        if self.future and not self.future.done():
            self.future.set_result(callable.response)