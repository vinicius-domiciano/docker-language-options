from typing import Type, TypeVar, Dict, Callable

T = TypeVar('T')

class EventListener:
    def __init__(self):
        self.listeners: Dict[Type, Callable[[object], None]] = {}

    def add_listener(self, cls: Type[T], listener: Callable[[T], None]) -> None:
        self.listeners[cls] = listener

    def emit(self, event: object):
        event_type = type(event)
        listener = self.listeners.get(event_type)

        if listener:
            listener(event)
        else:
            raise Exception("Não foi encontrado o listener para o objeto")