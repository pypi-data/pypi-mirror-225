
class BoxException(Exception):
    pass

class MissingGenericException(BoxException):
    def __init__(self, message="Generic Exception"):
        self.message = message
        super().__init__(self.message)