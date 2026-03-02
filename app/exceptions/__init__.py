# exceptions package: convenient re-exports for exception types and messages
from .auth import PermissionDenied, UnauthenticatedException
from .organisatie import (
    EXC_MSG_ORGANISATIE_PERMISSION_DENIED,
    EXC_MSG_ORGANISATIE_UNAUTHENTICATED,
    EXC_MSG_ORGANISATIE_NOT_FOUND,
    EXC_MSG_ORGANISATIE_EXISTS,
    OrganisatieException,
    OrganisatieExistsException,
    OrganisatiePermissionDenied,
    OrganisatieUnauthenticatedException,
)
from .persoon import (
    EXC_MSG_PERSOON_PERMISSION_DENIED,
    EXC_MSG_PERSOON_UNAUTHENTICATED,
    EXC_MSG_PERSOON_NOT_FOUND,
    EXC_MSG_PERSOON_EXISTS,
    PersoonException,
    PersoonExistsException,
    PersoonPermissionDenied,
    PersoonUnauthenticatedException,
)

__all__ = [
    "PermissionDenied",
    "UnauthenticatedException",

    # organisatie
    "EXC_MSG_ORGANISATIE_PERMISSION_DENIED",
    "EXC_MSG_ORGANISATIE_UNAUTHENTICATED",
    "EXC_MSG_ORGANISATIE_NOT_FOUND",
    "EXC_MSG_ORGANISATIE_EXISTS",
    "OrganisatieException",
    "OrganisatieExistsException",
    "OrganisatiePermissionDenied",
    "OrganisatieUnauthenticatedException",

    # persoon
    "EXC_MSG_PERSOON_PERMISSION_DENIED",
    "EXC_MSG_PERSOON_UNAUTHENTICATED",
    "EXC_MSG_PERSOON_NOT_FOUND",
    "EXC_MSG_PERSOON_EXISTS",
    "PersoonException",
    "PersoonExistsException",
    "PersoonPermissionDenied",
    "PersoonUnauthenticatedException",
]

# from fastapi import FastAPI
# from fastapi.exceptions import RequestValidationError
#
# from .handlers import validation_exception_handler
#
#
# def register_exception_handlers(app: FastAPI):
#     app.add_exception_handler(RequestValidationError, validation_exception_handler)