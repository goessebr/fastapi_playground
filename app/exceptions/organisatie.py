from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException
from app.exceptions.common import NotFoundException
from app.exceptions.common import ObjectExistsException

EXC_MSG_ORGANISATIE_PERMISSION_DENIED = (
    "Je hebt geen toegang tot deze organisatie resource."
)
EXC_MSG_ORGANISATIE_UNAUTHENTICATED = (
    "Je moet aangemeld zijn om deze organisatie resource te bekijken."
)
EXC_MSG_ORGANISATIE_NOT_FOUND = "Organisatie niet gevonden."
EXC_MSG_ORGANISATIE_EXISTS = "Organisatie bestaat reeds."


class OrganisatieNotFoundException(NotFoundException):
    def __init__(self, message=EXC_MSG_ORGANISATIE_NOT_FOUND):
        super().__init__(message)


class OrganisatieExistsException(ObjectExistsException):
    def __init__(self, message=EXC_MSG_ORGANISATIE_EXISTS):
        super().__init__(message)


class OrganisatiePermissionDenied(PermissionDenied):
    def __init__(self, message=EXC_MSG_ORGANISATIE_PERMISSION_DENIED):
        super().__init__(message)


class OrganisatieUnauthenticatedException(UnauthenticatedException):
    def __init__(self, message=EXC_MSG_ORGANISATIE_UNAUTHENTICATED):
        super().__init__(message)
