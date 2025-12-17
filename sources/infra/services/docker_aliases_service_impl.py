
from typing import override
from sources.app.services.docker_aliases_service import DockerAliasesService

from os.path import expanduser
from pathlib import Path

class DockerAliasesServiceImpl(DockerAliasesService):
    start_aliases_comment = "# __start_aliases_from_languages__"
    end_aliases_comment = "# __end_aliases_from_languages__"

    def __init__(self):
        self._aliases_line: list[str] = []
        self._begging_line: list[str] = []

        module_path = Path(__file__).resolve().parents[2]
        self._file_path = expanduser(f"{module_path}/bin/aliases.sh")
        
        self._prepare_aliases_line()
        super().__init__()

    def _prepare_aliases_line(self):
        have_already_found_start_line = False
        have_already_found_end_line = False

        all_lines: list[str] = []

        with open(self._file_path, 'r') as stream:
            all_lines.extend(stream.readlines())

        count = 0
    
        while not have_already_found_start_line or not have_already_found_end_line:
            if all_lines[count].startswith(self.start_aliases_comment):
                have_already_found_start_line = True
            elif have_already_found_start_line:
                self._aliases_line.append(all_lines[count].replace("\n", ""))
            else:
                self._begging_line.append(all_lines[count].replace("\n", ""))

            count += 1

            if count >= len(all_lines): 
                break 
            elif all_lines[count].startswith(self.end_aliases_comment):
                have_already_found_end_line = True
            
        if not have_already_found_start_line or not have_already_found_end_line:
            raise "Something went wrong while reading aliases"


    @override
    def update_aliases(self, image_name, command):
        have_already_founded = False

        count = 0
        while count < len(self._aliases_line):
            if self._aliases_line[count].startswith(f"alias {command}="):
                have_already_founded = True
                break

            count += 1

        alias_line = f"alias {command}='__docker_image_run__ {image_name} {command}'"

        if have_already_founded:
            self._aliases_line[count] = alias_line
        else:
            self._aliases_line.append(alias_line)

    @override
    def save_aliases(self):
        self._aliases_line.insert(0, self.start_aliases_comment)
        self._aliases_line.append(self.end_aliases_comment)

        with open(self._file_path, 'w') as stream:
            stream.write("\n".join([*self._begging_line, *self._aliases_line]))

    @override
    def contains_alias(self, image_name, alias):
        alias_line = f"alias {alias}='__docker_image_run__ {image_name} {alias}'"
        
        for line in self._aliases_line:
            if line == alias_line: return True

        return False