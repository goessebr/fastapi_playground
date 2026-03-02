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

def validate_read_access(
    service: BaseService,
    resource: ORMBase,
    current_user: dict | None = None,
) -> None:
    """
    Raise HTTP exceptions if resource is not found or user doesn't have read access to it.

    :param service:
    :param resource:
    :param current_user:
    :return:
    """
    validate_access(service.policies.assert_view_access, resource, current_user)

def validate_edit_access(
    service: BaseService,
    resource: ORMBase,
    current_user: dict,
) -> None:
    """
    Raise HTTP exceptions if resource is not found or user doesn't have read access to it.

    :param service:
    :param resource:
    :param current_user:
    :return:
    """
    validate_access(service.policies.assert_edit_access, resource, current_user)


def validate_access(
    assert_method: callable,
    resource: ORMBase,
    current_user: dict | None = None,
) -> None:
    """
    Raise HTTP exceptions if a user doesn't have access to a resource.

    :param assert_method:
    :param resource:
    :param current_user:
    :return:
    """
    try:
        assert_method(resource, current_user)
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
