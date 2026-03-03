from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException
from starlette import status

from app.exceptions.auth import PermissionDenied
from app.data.db.base import Base as ORMBase
from app.exceptions.auth import UnauthenticatedException

if TYPE_CHECKING:
    from app.services.base import BaseService


def assert_resource_exists(
    resource: ORMBase,
    msg_404: str = "resource niet gevonden",
) -> None:
    """
    Raise HTTP 404 exception if resource is not found.

    :param resource:
    :param msg_404:
    :return:
    """
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg_404,
        )
    return
