from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException
from app.exceptions.common import NotFoundException
from app.exceptions.common import ObjectExistsException

EXC_MSG_PERSOON_PERMISSION_DENIED = "Je hebt geen toegang tot deze persoon resource."
EXC_MSG_PERSOON_UNAUTHENTICATED = (
    "Je moet aangemeld zijn om deze persoon resource te bekijken."
)
EXC_MSG_PERSOON_NOT_FOUND = "Persoon niet gevonden."
EXC_MSG_PERSOON_EXISTS = "Persoon bestaat reeds."


class PersoonExistsException(ObjectExistsException):
    def __init__(self, message=EXC_MSG_PERSOON_EXISTS):
        super().__init__(message)


class PersoonNotFoundException(NotFoundException):
    def __init__(self, message=EXC_MSG_PERSOON_NOT_FOUND):
        super().__init__(message)


class PersoonPermissionDeniedException(PermissionDenied):
    def __init__(self, message=EXC_MSG_PERSOON_PERMISSION_DENIED):
        super().__init__(message)


class PersoonUnauthenticatedException(UnauthenticatedException):
    def __init__(self, message=EXC_MSG_PERSOON_UNAUTHENTICATED):
        super().__init__(message)
