
class CreateTokenException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenNotExistException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenInvalidException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DataAddressException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)