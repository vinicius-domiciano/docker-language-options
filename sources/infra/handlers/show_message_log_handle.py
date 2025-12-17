from sources.controller.show_message_log_controller import ShowMessageLogController, ShowMessageLogListenerCallable
from sources.services.event_listener import EventListener

class ShowMessageLogHandler:
    def __init__(self, controller: ShowMessageLogController, listener: EventListener):
        self.controller = controller
        listener.add_listener(ShowMessageLogListenerCallable, self.__show_log__)

    def __show_log__(self, message_callable: ShowMessageLogListenerCallable):
        self.controller.showLog(message_callable.message)