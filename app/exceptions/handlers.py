from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from app.exceptions import PermissionDenied
from app.exceptions import UnauthenticatedException
from app.exceptions.common import NotFoundException
from app.exceptions.common import ObjectExistsException
from app.exceptions.common import ValidationException


async def permission_denied_handler(request: Request, exc: PermissionDenied):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


async def not_found_handler(request: Request, exc: NotFoundException):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


async def unauthenticated_handler(request: Request, exc: UnauthenticatedException):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


async def object_exists_handler(request: Request, exc: ObjectExistsException):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


async def validation_exception_handler(request: Request, exc: ObjectExistsException):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


def register_exception_handlers(app):
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(PermissionDenied, permission_denied_handler)
    app.add_exception_handler(UnauthenticatedException, unauthenticated_handler)
    app.add_exception_handler(ObjectExistsException, object_exists_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
