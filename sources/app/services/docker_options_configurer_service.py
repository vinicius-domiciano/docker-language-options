from abc import ABC, abstractmethod

class DockerOptionsConfigurerService(ABC): 
    def __init__(self):
        pass

    @abstractmethod
    def get_languages_properties(self, propert_name: str) -> dict:
        pass

    @abstractmethod
    def verify_language_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def add_new_version(self, name: str, version_opt: dict) -> None:
        pass
    
    @abstractmethod
    def add_new_language(self, name: str) -> None:
        pass
    
    @abstractmethod
    def remove_language(self, name: str) -> None:
        pass
    
    @abstractmethod
    def remove_version(self, language: str, version: str) -> None:
        pass