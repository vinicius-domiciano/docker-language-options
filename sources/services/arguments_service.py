from argparse import Namespace
from sources.app.models.argument import ArgumentParams
from os.path import expanduser
import json

class ArgumentService:
    def __init__(self):
        self.argument = ArgumentParams()

    def load(self, args: Namespace):
        params = dict(args._get_kwargs())

        json_type = params.get("type")
        json_file_path = params.get("file_path")
        json_value = params.get("json")

        if json_type == "JSON":
            self._load_by_json(json_value)
        elif json_type == "JSON_PATH":
            self._get_by_path(json_file_path)
        else:
            raise Exception("O comando type informado esta invalido")

    def _prepare_json(self, json_value: str):
        if not json_value:
            raise Exception("O json informado esta invalido")
        
        self._load_by_json(json.loads(json_value))
        
    def _get_by_path(self, json_path):
        if not json_path:
            raise Exception("Json path esta invalido")
        
        json_path = expanduser(json_path)
        with open(json_path, 'rb') as stream:
            self._load_by_json(json.loads(stream.read()))

    def _load_by_json(self, values: dict):
        self.argument.language = values['language']
        self.argument.version = values['version']
        self.argument.programs_to_install = values.get('programs-required')
        self.argument.url = values.get('langauge-url')
        self.argument.executable_path = values.get('executable-path')
        self.argument.envs = values.get('envs')
        self.argument.use_image = values.get('use-image')
        self.argument.image_name = values.get('image-name')
        self.argument.aliases = values['aliases']
