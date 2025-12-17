from sources.controller.change_version_controller import ChangeVersionController
from sources.controller.configure_project_controller import ConfigureProjectController
from sources.controller.remove_language_controller import RemoveLanguageController
from sources.controller.remove_version_controller import RemoveVersionController
from sources.infra.dependecy_injection import di
from sources.controller.show_message_log_controller import ShowMessageLogListenerCallable
from sources.controller.command_execute_controller import CommandExecuteController
from sources.controller.new_language_controller import NewLanguageController
from sources.controller.new_version_controller import NewVersionController
from sources.services.event_listener import EventListener
from sources.services.arguments_service import ArgumentService
import argparse

class __DockerLanguageOptions__:
    
    @staticmethod
    def start_di_and_get_controller(arguments: argparse.Namespace) -> CommandExecuteController:
        start_injection = di.StartInjectionFromOption()
        di.get(EventListener).emit(ShowMessageLogListenerCallable("Injetando dependencias"))

        match arguments.option:
            case "new:language":
                start_injection.inject_from_new_language()
                return NewLanguageController(arguments.language)
            case "new:version":
                start_injection.inject_from_new_version()
                di.get(ArgumentService).load(arguments)
                return NewVersionController()
            case "rm:language":
                start_injection.inject_from_remove_language()
                return RemoveLanguageController(arguments.language)
            case "rm:version":
                start_injection.inject_from_remove_version()
                return RemoveVersionController(arguments.language, arguments.version)
            case "ch:version":
                start_injection.inject_from_change_version()
                return ChangeVersionController(arguments.language, arguments.version)
            case "conf:prepare":
                start_injection.inject_from_configure_program()
                return ConfigureProjectController()
            case _:
                raise Exception('Falha. Não existe o comando informado')

class __Main__():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--option", help="Command Required to run", choices=["new:language", "new:version", "rm:language","rm:version", "ch:version", "conf:prepare"], required=True)
        parser.add_argument("--type", help="type of value", choices=['JSON', 'JSON_PATH'], required=False)
        parser.add_argument("--language", help="Name of language in languages.yaml file", required=False)
        parser.add_argument("--version", help="Name of version in languages.yaml file", required=False)
        parser.add_argument("--file_path", help="Path from .json file, use when [-t is JSON]", required=False)
    
        parsed = parser.parse_args()
        self.command_controller = __DockerLanguageOptions__.start_di_and_get_controller(parsed)

        di.get(EventListener).emit(ShowMessageLogListenerCallable("Dependencias injetadas"))

    def start(self):
        di.get(EventListener).emit(ShowMessageLogListenerCallable("Iniciando use_case"))
        self.command_controller.execute()

if __name__ == "__main__":
    try:
        __Main__().start()
    except Exception as e:
        print(f"Alguma coisa inexperada aconteceu!\nStacktrace: {e}")
        pass
