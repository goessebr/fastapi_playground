from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException

EXC_MSG_ORGANISATIE_PERMISSION_DENIED = "Je hebt geen toegang tot deze organisatie resource."
EXC_MSG_ORGANISATIE_UNAUTHENTICATED = "Je moet aangemeld zijn om deze organisatie resource te bekijken."
EXC_MSG_ORGANISATIE_NOT_FOUND = "Organisatie niet gevonden."
EXC_MSG_ORGANISATIE_EXISTS = "Organisatie bestaat reeds."

class OrganisatieException(Exception):
    pass

class OrganisatieExistsException(OrganisatieException):
    pass

class OrganisatiePermissionDenied(PermissionDenied):
    def __init__(self, message=EXC_MSG_ORGANISATIE_PERMISSION_DENIED):
        super().__init__(message)

class OrganisatieUnauthenticatedException(UnauthenticatedException):
    def __init__(self, message=EXC_MSG_ORGANISATIE_UNAUTHENTICATED):
        super().__init__(message)