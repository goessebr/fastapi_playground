from fastapi import HTTPException
from starlette import status

from app.data.db.base import Base as ORMBase
from app.exceptions.auth import PermissionDenied
from app.exceptions.auth import UnauthenticatedException
from app.services.base import BaseService


def validate_acces(
        service: BaseService,
        object: ORMBase,
        current_user: dict,
        msg_404: str = "Object niet gevonden",
    ) -> None:
    """
    Raise HTTP exceptions if object is not found or user doesn't have access to it.

    :param service:
    :param object:
    :param current_user:
    :return:
    """
    if not object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg_404,
        )
    try:
        service.policies.assert_view(object, current_user)
    except UnauthenticatedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except PermissionDenied as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    return