from sources.app.services.docker_options_configurer_service import DockerOptionsConfigurerService
import yaml
from os.path import expanduser
from pathlib import Path

class DockerOptionsConfigurerServiceImpl(DockerOptionsConfigurerService):
    def __init__(self):
        super().__init__()
        self.docker_options = {}
        self.file_path = ""
        
        self.__load_file_path__()
        self.__open__()

    def  __load_file_path__(self):  
        module_path = Path(__file__).resolve().parents[2]
        self.file_path = expanduser(f"{module_path}/settings/languages.yaml")
    
    def __open__(self):
        with open(self.file_path, 'r') as stream:
            try:
                self.docker_options = yaml.safe_load(stream)
            except:
                pass

    def __update_file__(self):
        with open(self.file_path, 'w') as stream:
            stream.writelines(yaml.dump(self.docker_options))

    def get_languages_properties(self, propert_name) -> dict:
        language_opt: dict = self.docker_options.get("languages")
        return language_opt.get(propert_name)

    def verify_language_exists(self, name):
        language_opt: dict = self.docker_options.get("languages")
        return name in language_opt

    def add_new_version(self, name, version_opt):
        language_opt = self.get_languages_properties(name)
        language_opt.update(version_opt)
        self.docker_options['languages'][name] = language_opt
        
        self.__update_file__()

    def add_new_language(self, name):
        languages: dict = self.docker_options.get('languages')
        languages.update({ name: {} })

        self.__update_file__()

    def remove_language(self, name):
        languages: dict = self.docker_options.get('languages')
        languages.pop(name)
        self.docker_options['languages'] = languages

        self.__update_file__()

    def remove_version(self, language, version):
        language_opt: dict = self.docker_options.get('languages').get(language)
        language_opt.pop(version)

        self.docker_options['languages'][language] = language_opt

        self.__update_file__()
        