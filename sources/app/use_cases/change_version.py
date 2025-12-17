
from abc import ABC, abstractmethod
import asyncio
from typing import override

from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService


class ChangeVersionOutputPort(ABC):

    @abstractmethod
    async def can_change_version_from_language(self, version_name: str, language_name: str) : pass

    @abstractmethod
    def on_error(self, message: str): pass

    @abstractmethod
    def on_success(self, image_name: str, aliases: list[str]): pass

class ChangeVersionInputPort(ABC):

    @abstractmethod
    def execute(self, version_name: str, language_name: str, output_port: ChangeVersionOutputPort): pass

class ChangeVersionImpl(ChangeVersionInputPort):
    def __init__(self, language_service: DockerOptionsConfigurerService):
        self.language_service = language_service

    @override
    def execute(self, version_name, language_name, output_port):
        if not version_name or version_name == "":
            output_port.on_error("A versão informada está invalida!")
            return
        elif not language_name or language_name == "":
            output_port.on_error("A linguagem informada está invalida!")
            return

        language = self.language_service.get_languages_properties(language_name)
        if not language:
            output_port.on_error(f"A linguagem: [{language_name}], não foi encontrada")
            return

        version: dict = language.get(version_name)
        if not version:
            output_port.on_error(f"A versão: [{version_name}], não foi encontrada")
            return

        can_change_version: bool = asyncio.run(output_port.can_change_version_from_language(
            version_name, 
            language_name
        ))

        if can_change_version:
            output_port.on_success(version.get("image_name"), version.get("alias"))
        else:
            output_port.on_error("Encerrando o processo")