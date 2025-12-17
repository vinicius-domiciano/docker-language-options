from typing import override
from sources.app.services.docker_image_service import DockerImageService
from os.path import expanduser
from pathlib import Path

class DockerImageServiceImpl(DockerImageService):
    __LANGUAGE_URL__ = "__LANGUAGE_URL__"
    __EXECUTABLE_PATH__ = "__EXECUTABLE_PATH__"
    __APT_GET_REQUIRED__ = "__APT_GET_REQUIRED__"
    __LANGUAGE__ = "__LANGUAGE__"
    __LOAD_ENVS__ = "__LOAD_ENVS__"

    def __init__(self):
        self.languages_file_path = ""
        self.dockerfile_base_path = ""
        self.__load_file_path__()

        self.dockerfile_base_lines: list[str]
        self.__load_docker_file_base_lines__()

    def  __load_file_path__(self):
        module_path = Path(__file__).resolve().parents[2]
        self.languages_file_path = expanduser(f"{module_path}/settings/languages.yaml")
        self.dockerfile_base_path = expanduser(f"{module_path}/settings/dockerfile.initialization-machine")

    def __load_docker_file_base_lines__(self):
        with open(self.dockerfile_base_path, 'r') as stream:
            self.dockerfile_base_lines = stream.readlines()

    def __create_file__(self, file_name:str):
        module_path = Path(__file__).resolve().parents[2]
        file_path = expanduser(f'{module_path}/settings/build/{file_name}')
        with open(file_path, 'w+') as stream:
            stream.writelines(self.dockerfile_base_lines)

    def __replace_key__(self, line: str, key: str, value: str):
        return line.replace(key, value)

    def __change_file_keys__(self, key:str, value:str):
        changed_lines = list(map(
            lambda line : self.__replace_key__(line, key, value),
            self.dockerfile_base_lines
        ))

        self.dockerfile_base_lines.clear()
        self.dockerfile_base_lines.extend(changed_lines)

    @override
    def create_image_file(self, request):
        self.__change_file_keys__(self.__LANGUAGE_URL__, request.language_url)
        self.__change_file_keys__(self.__EXECUTABLE_PATH__, request.executable_path)
        self.__change_file_keys__(self.__APT_GET_REQUIRED__, " ".join(request.required_libs))
        self.__change_file_keys__(self.__LANGUAGE__, request.language_name)
        self.__change_file_keys__(self.__LOAD_ENVS__, "\n".join(request.adjusted_envs))

        self.__create_file__(request.file_name)

    def create_volume_name(self, language: str, version: str):
        pass