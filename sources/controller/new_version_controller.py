
from typing import override
from sources.app.use_cases.build_docker_file import BuildDockerFileInputPort, BuildDockerFileOutputPort
from sources.app.use_cases.create_docker_file import CreateDockerFileInputPort, CreateDockerFileOutputPort
from sources.app.use_cases.download_image import DownloadImageInputPort, DownloadImageOutputPort
from sources.app.use_cases.update_aliases import UpdateAliasesInputPort, UpdateAliasesOutputPort
from sources.controller.command_execute_controller import CommandExecuteController
from sources.app.use_cases.add_new_version import AddNewVersionInputPort, AddNewVersionOutputPort
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.infra.dependecy_injection.di import get
from sources.services.arguments_service import ArgumentService
from sources.services.event_listener import EventListener
from sources.app.models.argument import ArgumentParams

class NewVersionController(CommandExecuteController):
    _argument: ArgumentParams

    def __init__(self):
        self.image_name = ""

    @override
    def execute(self):
        self._argument = get(ArgumentService).argument

        get(AddNewVersionInputPort).execute(
            arguments=self._argument,
            output_port=_AddNewVersionPresenter(self)
        )

    def create_docker_file(self):
        get(CreateDockerFileInputPort).execute(
            output_port=_CreateDockerFilePresenter(self),
            argument=self._argument
        )

    def build_image(self):
        get(BuildDockerFileInputPort).execute(
            image_name=self.image_name,
            output_port=_BuildDockerFilePresenter(self)
        )

    def download_image(self):
        get(DownloadImageInputPort).execute(
            image_name=self._argument.image_name,
            output_port=_BuildDockerFilePresenter(self)
        )

    def update_aliases(self):
        get(UpdateAliasesInputPort).execute(
            image_name=self.image_name,
            aliases=self._argument.aliases,
            output_port=_UpdateAliasesPresenter(self)
        )

    def finish(self):
        get(EventListener).emit(ShowMessageLogListenerCallable("Nova versão adicionada com sucesso"))


class _UpdateAliasesPresenter(UpdateAliasesOutputPort):
    def __init__(self, controller: NewVersionController):
        self.controller = controller

    @override
    def on_success(self):
        self.controller.finish()

class _BuildDockerFilePresenter(BuildDockerFileOutputPort, DownloadImageOutputPort):
    def __init__(self, controller: NewVersionController):
        self.controller = controller

    @override
    def on_success(self, image_name):
        self.controller.image_name = image_name
        self.controller.update_aliases()


class _CreateDockerFilePresenter(CreateDockerFileOutputPort):
    def __init__(self, controller: NewVersionController):
        self.controller = controller
    
    @override
    def on_success(self, image_name):
        self.controller.image_name = image_name
        self.controller.build_image()


class _AddNewVersionPresenter(AddNewVersionOutputPort):
    def __init__(self, controller: NewVersionController):
        self.controller = controller

    @override
    def on_success(self, image_name):
        if self.controller._argument.use_image:
            self.controller.download_image()
        else:
            self.controller._argument.image_name = image_name
            self.controller.create_docker_file()

    @override
    def on_failure(self, message):
        get(EventListener).emit(ShowMessageLogListenerCallable(message))
