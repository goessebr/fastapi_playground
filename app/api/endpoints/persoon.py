from typing import Annotated

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.dependencies import get_persoon_presenter
from app.api.dependencies import get_persoon_service
from app.api.endpoints.auth import CurrentUserDependency
from app.api.endpoints.fastapi_oeutils import assert_object_exists
from app.api.endpoints.fastapi_oeutils import validate_read_access
from app.api.responses import RESPONSES_GET_PERSOON
from app.api.responses import RESPONSES_POST_PERSOON
from app.exceptions.persoon import EXC_MSG_PERSOON_EXISTS
from app.exceptions.persoon import EXC_MSG_PERSOON_NOT_FOUND
from app.exceptions.persoon import PersoonExistsException
from app.presenters.persoon import PersoonPresenter
from app.schemas.persoon import PersoonCreate
from app.schemas.persoon import PersoonResponse
from app.services.persoon import PersoonService


from app.core.logging import get_logger

LOG = get_logger(__name__)

router = APIRouter()


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
    assert_object_exists(persoon, msg_404=EXC_MSG_PERSOON_NOT_FOUND)
    validate_read_access(service, persoon, current_user)
    return presenter.present(persoon, current_user)
