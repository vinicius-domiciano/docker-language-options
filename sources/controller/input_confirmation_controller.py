from sources.services.event_listener import EventListener

class RequestInputConfirmationControllerCallable:
    def __init__(self, message: str):
        self.message = message


class ResponseInputConfirmationControllerCallable:
    def __init__(self, response: bool):
        self.response = response


class InputConfirmationController:
    def __init__(self, listener: EventListener):
        self.listener = listener
        self.__register_listener__()

    def __register_listener__(self):
        self.listener.add_listener(
            cls=RequestInputConfirmationControllerCallable,
            listener=self.request
        )

    def request(self, callable: RequestInputConfirmationControllerCallable):
        intput_value = input(f'{callable.message}').strip().lower()
        response = intput_value == "s"

        self.listener.emit(ResponseInputConfirmationControllerCallable(response))