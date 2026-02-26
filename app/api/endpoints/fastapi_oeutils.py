from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException
from starlette import status

from app.exceptions.auth import PermissionDenied
from app.data.db.base import Base as ORMBase
from app.exceptions.auth import UnauthenticatedException

if TYPE_CHECKING:
    from app.services.base import BaseService


class AccessTypes:
    VIEW = "view"
    EDIT = "edit"


def assert_object_exists(
    object: ORMBase,
    msg_404: str = "Object niet gevonden",
) -> None:
    """
    Raise HTTP 404 exception if object is not found.

    :param object:
    :param msg_404:
    :return:
    """
    if not object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg_404,
        )
    return


def validate_access(
    access_type: str,
    service: BaseService,
    object: ORMBase,
    current_user: dict,
) -> None:
    """
    Raise HTTP exceptions if object is not found or user doesn't have access to it.

    :param access_type:
    :param service:
    :param object:
    :param current_user:
    :return:
    """
    try:
        service.policies.assert_access(access_type, object, current_user)
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
