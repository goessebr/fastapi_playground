from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException


class PersoonException(Exception):
    pass

class PersoonExistsException(PersoonException):
    pass

class PersoonPermissionDenied(PermissionDenied):
    def __init__(self, message="Je hebt geen toegang tot deze persoon resource."):
        super().__init__(message)

class PersoonUnauthenticatedException(UnauthenticatedException):
    def __init__(self, message="Je moet ingelogd zijn om deze persoon resource te bekijken."):
        super().__init__(message)