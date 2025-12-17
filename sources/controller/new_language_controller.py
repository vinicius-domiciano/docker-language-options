from sources.controller.command_execute_controller import CommandExecuteController
from sources.infra.dependecy_injection.di import get
from sources.app.use_cases.add_new_language import AddNewLanguageInputPort

class NewLanguageController(CommandExecuteController):
    def __init__(self, language_name: str):
        self.language_name = language_name

    def execute(self):
        get(AddNewLanguageInputPort).execute(name=self.language_name)