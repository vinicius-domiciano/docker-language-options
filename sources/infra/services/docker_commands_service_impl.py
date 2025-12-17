from typing import override

from sources.app.services.docker_commands_service import DockerCommandsService
from subprocess import run
from os.path import expanduser
from pathlib import Path

class DockerCommandsServiceImpl(DockerCommandsService):
    DOCKER_COMMANDS_PATHS = 'bin/docker_functions.sh'

    def __init__(self):
        self.function_path = ""
        self.language_up_path = ""
        self._open_docker_functions_bash()

    def _open_docker_functions_bash(self):
        module_path = Path(__file__).resolve().parents[2]
        self.language_up_path = expanduser(f"{module_path}/settings/build/dockerfile.language-up")
        self.function_path = expanduser(f"{module_path}/{self.DOCKER_COMMANDS_PATHS}")

    def _run_commands(self, commands: list[str]):
        prepared_command = " ".join(['source', self.function_path, "&&", *commands])

        run(['bash', '-c', prepared_command], check=True, executable="/bin/bash")

    @override
    def build_docker_file(self, image_name):
        self._run_commands(['__create_image_from_docker_file_function__', image_name, self.language_up_path])

    @override
    def pull_image(self, image_name):
        self._run_commands(['__download_image_from_docker_file_function__', image_name])