from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException

EXC_MSG_PERSOON_PERMISSION_DENIED = "Je hebt geen toegang tot deze persoon resource."
EXC_MSG_PERSOON_UNAUTHENTICATED = "Je moet aangemeld zijn om deze persoon resource te bekijken."
EXC_MSG_PERSOON_NOT_FOUND = "Persoon niet gevonden."
EXC_MSG_PERSOON_EXISTS = "Persoon bestaat reeds."

class PersoonException(Exception):
    pass

class PersoonExistsException(PersoonException):
    pass

class PersoonPermissionDenied(PermissionDenied):
    def __init__(self, message=EXC_MSG_PERSOON_PERMISSION_DENIED):
        super().__init__(message)

class PersoonUnauthenticatedException(UnauthenticatedException):
    def __init__(self, message=EXC_MSG_PERSOON_UNAUTHENTICATED):
        super().__init__(message)