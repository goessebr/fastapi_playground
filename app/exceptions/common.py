class NotFoundException(Exception):
    pass


class ObjectExistsException(Exception):
    pass

class ValidationException(Exception):
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.errors = errors or {}