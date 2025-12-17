
from abc import ABC, abstractmethod
import asyncio

from sources.app.services.docker_project_configurer_service import DockerProjectConfigurerService


class ConfigureProjectOutputPort(ABC): 

    @abstractmethod
    async def can_continue(self): pass

    @abstractmethod
    def on_success(self): pass

class ConfigureProjectInputPort(ABC):

    @abstractmethod
    def execute(self, output_port: ConfigureProjectOutputPort): pass

class ConfigureProjectImpl(ConfigureProjectInputPort):
    def __init__(self, project_configurer_service: DockerProjectConfigurerService):
        self.project_configurer_service = project_configurer_service

    def execute(self, output_port):
        can_continue = asyncio.run(output_port.can_continue())
        if can_continue:
            self.project_configurer_service.generate_alias()
            self.project_configurer_service.run_configurer()
        
        output_port.on_success()
