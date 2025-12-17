
class ArgumentParams:
    def __init__(self):
        self.language = ""
        self.version = ""
        self.programs_to_install: list[str] = []
        self.url = ""
        self.executable_path = ""
        self.envs: list[str] = []
        self.aliases: list[str] = []
        self.use_image = False
        self.image_name = ""