from typing import Type, TypeVar, Dict

from sources.app.services.docker_aliases_service import DockerAliasesService
from sources.app.services.docker_commands_service import DockerCommandsService
from sources.app.services.docker_image_service import DockerImageService
from sources.app.services.docker_project_configurer_service import DockerProjectConfigurerService
from sources.app.use_cases.add_new_version import AddNewVersionInputPort, AddNewVersion
from sources.app.use_cases.add_new_language import AddNewLanguageInputPort, AddNewLanguage
from sources.app.use_cases.build_docker_file import BuildDockerFile, BuildDockerFileInputPort
from sources.app.use_cases.change_version import ChangeVersionImpl, ChangeVersionInputPort
from sources.app.use_cases.configure_project import ConfigureProjectImpl, ConfigureProjectInputPort
from sources.app.use_cases.create_docker_file import CreateDockerFileInputPort, CreateDockerFile
from sources.app.use_cases.download_image import DownloadImageInputPort, DownloadImageImpl
from sources.app.use_cases.remove_language import RemoveLanguageInputPort, RemoveLanguage
from sources.app.use_cases.remove_version import RemoveVersionInputPort, RemoveVersion
from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService
from sources.app.use_cases.update_aliases import UpdateAliasesInputPort, UpdateAliasesImpl
from sources.controller.input_confirmation_controller import InputConfirmationController
from sources.controller.show_message_log_controller import ShowMessageLogController
from sources.infra.handlers.show_message_log_handle import ShowMessageLogHandler
from sources.infra.services.docker_aliases_service_impl import DockerAliasesServiceImpl
from sources.infra.services.docker_commands_service_impl import DockerCommandsServiceImpl
from sources.infra.services.docker_image_service_impl import DockerImageServiceImpl
from sources.infra.services.docker_option_configurer_impl import DockerOptionsConfigurerServiceImpl
from sources.infra.services.docker_project_configurer_service_impl import DockerProjectConfigurerServiceImpl
from sources.services.event_listener import EventListener
from sources.services.arguments_service import ArgumentService

T = TypeVar('T')
__instances__: Dict[Type[object], object] = {}

def __register_by_instance__(instance: object):
    event_type = type(instance)
    __instances__[event_type] = instance

def __register__(cls: Type[T], instance: T):
    __instances__[cls] = instance

def get(cls: Type[T]) -> T:
    return __instances__.get(cls)

class _BaseInjection:
   def start(self):
       __register_by_instance__(EventListener())
       __register_by_instance__(ShowMessageLogController())
       __register_by_instance__(ArgumentService())
       ShowMessageLogHandler(controller=get(ShowMessageLogController), listener=get(EventListener))

class _StartFromNewLanguage:
    def __init__(self):
        __register__(
            cls=DockerOptionsConfigurerService,
            instance=DockerOptionsConfigurerServiceImpl()
        )

        __register__(
            cls=AddNewLanguageInputPort,
            instance=AddNewLanguage(
                listener=get(EventListener),
                docker_options_service=get(DockerOptionsConfigurerService)
            )
        )

class _StartFromNewVersion:
    def __init__(self):
        __register__(
            cls=DockerOptionsConfigurerService,
            instance=DockerOptionsConfigurerServiceImpl()
        )

        __register__(
            cls=DockerImageService,
            instance=DockerImageServiceImpl()
        )

        __register__(
            cls=DockerCommandsService,
            instance=DockerCommandsServiceImpl()
        )

        __register__(
            cls=DockerAliasesService,
            instance=DockerAliasesServiceImpl()
        )

        __register__(
            cls=AddNewVersionInputPort,
            instance=AddNewVersion(
                listener=get(EventListener),
                docker_options_service=get(DockerOptionsConfigurerService)
            )
        )

        __register__(
            cls=CreateDockerFileInputPort,
            instance=CreateDockerFile(
                listener=get(EventListener),
                docker_image_service=get(DockerImageService)
            )
        )

        __register__(
            cls=BuildDockerFileInputPort,
            instance=BuildDockerFile(
                listener=get(EventListener),
                commands_service=get(DockerCommandsService)
            )
        )

        __register__(
            cls=UpdateAliasesInputPort,
            instance=UpdateAliasesImpl(
                listener=get(EventListener),
                service=get(DockerAliasesService)
            )
        )

        __register__(
            cls=DownloadImageInputPort,
            instance=DownloadImageImpl(
                commands_service=get(DockerCommandsService)
            )
        )


class _StartFromRemoveLanguage:
    def __init__(self):
        __register_by_instance__(InputConfirmationController(
            listener=get(EventListener)
        ))

        __register__(
            cls=DockerAliasesService,
            instance=DockerAliasesServiceImpl()
        )

        __register__(
            cls=DockerOptionsConfigurerService,
            instance=DockerOptionsConfigurerServiceImpl()
        )

        __register__(
            cls=RemoveLanguageInputPort,
            instance=RemoveLanguage(
                listener=get(EventListener),
                docker_options_service=get(DockerOptionsConfigurerService),
                alias_service=get(DockerAliasesService)
            )
        )

class _StartFromRemoveVersion:
    def __init__(self):
        __register_by_instance__(InputConfirmationController(
            listener=get(EventListener)
        ))
        
        __register__(
            cls=DockerOptionsConfigurerService,
            instance=DockerOptionsConfigurerServiceImpl()
        )

        __register__(
            cls=DockerAliasesService,
            instance=DockerAliasesServiceImpl()
        )

        __register__(
            cls=RemoveVersionInputPort,
            instance=RemoveVersion(
                listener=get(EventListener),
                docker_options_service=get(DockerOptionsConfigurerService),
                alias_service=get(DockerAliasesService)
            )
        )

class _StartFromChangeVersion():
    def __init__(self):
        __register_by_instance__(InputConfirmationController(
            listener=get(EventListener)
        ))
        
        __register__(
            cls=DockerOptionsConfigurerService,
            instance=DockerOptionsConfigurerServiceImpl()
        )

        __register__(
            cls=DockerAliasesService,
            instance=DockerAliasesServiceImpl()
        )

        __register__(
            cls=ChangeVersionInputPort,
            instance=ChangeVersionImpl(
                language_service=get(DockerOptionsConfigurerService)
            )
        )

        __register__(
            cls=UpdateAliasesInputPort,
            instance=UpdateAliasesImpl(
                listener=get(EventListener),
                service=get(DockerAliasesService)
            )
        )

class _StartFromConfigureProgram:
    def __init__(self):
        __register_by_instance__(InputConfirmationController(
            listener=get(EventListener)
        ))
        
        __register__(
            cls=DockerProjectConfigurerService,
            instance=DockerProjectConfigurerServiceImpl()   
        )

        __register__(
            cls=ConfigureProjectInputPort,
            instance=ConfigureProjectImpl(
                get(DockerProjectConfigurerService)
            )
        )

class StartInjectionFromOption(_BaseInjection):
    def __init__(self): super().start()

    def inject_from_new_language(self): _StartFromNewLanguage()

    def inject_from_new_version(self): _StartFromNewVersion()

    def inject_from_remove_language(self): _StartFromRemoveLanguage()

    def inject_from_remove_version(self): _StartFromRemoveVersion()

    def inject_from_change_version(self): _StartFromChangeVersion()

    def inject_from_configure_program(self): _StartFromConfigureProgram()