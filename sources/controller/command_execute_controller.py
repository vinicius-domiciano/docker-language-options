from abc import ABC, abstractmethod

class CommandExecuteController(ABC):

    @abstractmethod
    def execute(self) -> None: pass
