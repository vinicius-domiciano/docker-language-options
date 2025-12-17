class ShowMessageLogController:
    
    def showLog(self, message: str):
        print(f'{message}')

class ShowMessageLogListenerCallable:
    def __init__(self, message: str):
        self.message = message
