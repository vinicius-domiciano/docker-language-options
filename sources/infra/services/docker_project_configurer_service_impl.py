
from sources.app.services.docker_project_configurer_service import DockerProjectConfigurerService
from typing import override

from os.path import expanduser
from pathlib import Path
from subprocess import run

__ALIAS_LINE__ = 'alias reload_aliases="$PATH"\n'

__IMAGE_RUN_FUNCTION__ = [
    '__docker_image_run__() {',
    '\tcontainer="$1"',
    '\tpath="$(pwd)"',
    '\tshift',
    '\tdocker run --rm -v "$path":/app -w /app "$container" "$@"',
    '}\n'
]

__ALIAS_BLOCK__ = "\n# __start_aliases_from_languages__\n# __end_aliases_from_languages__\n"

class DockerProjectConfigurerServiceImpl(DockerProjectConfigurerService):

    def __init__(self):
        module_path = Path(__file__).resolve().parents[2]
        self.alias_file_path = expanduser(f"{module_path}/bin/aliases.sh")
        self.configure_file_path = expanduser(f"{module_path}/bin/configure.sh")

    def _remove_alias_file_if_exists(self):
        file_path = Path(self.alias_file_path)

        try:
            file_path.unlink(missing_ok=True)
        except PermissionError:
            raise f"Permissão negada: não foi possivel remover o aquivo alias existente"

    def _create_file(self, lines: list[str]):
        with open(self.alias_file_path, 'w+') as stream:
            stream.write("\n".join(lines))

    @override
    def generate_alias(self):
        self._remove_alias_file_if_exists()

        lines: list[str] = [
            "#!/bin/bash\n",
            "### reload_aliases",
            __ALIAS_LINE__.replace("$PATH", f'source {self.alias_file_path}'),    
            "### Image run function",
            "\n".join(__IMAGE_RUN_FUNCTION__),
            __ALIAS_BLOCK__
        ]

        self._create_file(lines)

    @override
    def run_configurer(self):
        prepared_command = f"source {self.configure_file_path}"
        run(['bash', '-c', prepared_command], check=True, executable="/bin/bash")