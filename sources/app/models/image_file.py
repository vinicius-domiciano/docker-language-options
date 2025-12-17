class ImageFile():
    def __init__(self):
        self.image_name = ''
        self.container_name = ''
        self.language_name = ''
        self.environments: list[str] = []
        self.language_url = ''
        self.executable_path = '',
        self.required_libs: list[str] = []
        self.file_name = ''

    @property
    def adjusted_envs(self) -> list[str]:
        return list(map(lambda env: f"ENV {env}", self.environments))