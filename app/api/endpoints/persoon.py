from typing import Annotated

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.dependencies import get_persoon_presenter
from app.api.dependencies import get_persoon_service
from app.api.endpoints.auth import CurrentUserDependency
from app.api.endpoints.fastapi_oeutils import validate_acces
from app.exceptions.persoon import EXC_MSG_PERSOON_EXISTS
from app.exceptions.persoon import EXC_MSG_PERSOON_NOT_FOUND
from app.exceptions.persoon import EXC_MSG_PERSOON_PERMISSION_DENIED
from app.exceptions.persoon import EXC_MSG_PERSOON_UNAUTHENTICATED
from app.exceptions.persoon import PersoonExistsException
from app.presenters.persoon import PersoonPresenter
from app.schemas.persoon import PersoonCreate
from app.schemas.persoon import PersoonResponse
from app.services.persoon import PersoonService


from app.core.logging import get_logger

LOG = get_logger(__name__)

router = APIRouter()

RESPONSES_POST_PERSOON: dict = {
    400: {
        "description": "Validatiefout bij het aanmaken van persoon",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_EXISTS}}
        },
    }
}

RESPONSES_GET_PERSOON: dict = {
    401: {
        "description": "Niet geauthenticeerd",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_UNAUTHENTICATED}}
        },
    },
    403: {
        "description": "Geen toegang tot deze persoon",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_PERMISSION_DENIED}}
        },
    },
    404: {
        "description": EXC_MSG_PERSOON_NOT_FOUND,
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_NOT_FOUND}}
        },
    },
}


@router.post(
    "",
    response_model=PersoonResponse,
    status_code=status.HTTP_201_CREATED,
    responses=RESPONSES_POST_PERSOON,
)
async def create_persoon(
    persoon_data: PersoonCreate,
    service: Annotated[PersoonService, Depends(get_persoon_service)],
    current_user: CurrentUserDependency,
):
    try:
        return await service.create_persoon(persoon_data, created_by=current_user)
    except PersoonExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EXC_MSG_PERSOON_EXISTS,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get(
    "/{persoon_id}",
    response_model=PersoonResponse,
    responses=RESPONSES_GET_PERSOON,
)
async def get_persoon(
    persoon_id: int,
    service: Annotated[PersoonService, Depends(get_persoon_service)],
    current_user: CurrentUserDependency,
    presenter: PersoonPresenter = Depends(get_persoon_presenter),
):
    persoon = await service.get_persoon(persoon_id)
    validate_acces(service, persoon, current_user, msg_404=EXC_MSG_PERSOON_NOT_FOUND)
    return presenter.present(persoon, current_user)
