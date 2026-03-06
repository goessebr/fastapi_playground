from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.dependencies import CurrentUserDependency
from app.api.dependencies import ExistingPersoonDependency
from app.api.dependencies import assert_persoon_create_access
from app.api.dependencies import assert_persoon_view_access
from app.api.dependencies import get_persoon_presenter
from app.api.dependencies import get_persoon_service
from app.api.responses import RESPONSES_GET_PERSOON
from app.api.responses import RESPONSES_POST_PERSOON
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
    dependencies=[Depends(assert_persoon_create_access)],
)
async def create_persoon(
    persoon_data: PersoonCreate,
    service: Annotated[PersoonService, Depends(get_persoon_service)],
    current_user: CurrentUserDependency,
    presenter: PersoonPresenter = Depends(get_persoon_presenter),
):
    new = await service.create_persoon(persoon_data, created_by=current_user)
    return presenter.present(new, current_user)


@router.get(
    "/{persoon_id}",
    response_model=PersoonResponse,
    responses=RESPONSES_GET_PERSOON,
    dependencies=[Depends(assert_persoon_view_access)],
)
async def get_persoon(
    current_user: CurrentUserDependency,
    existing_persoon: ExistingPersoonDependency,
    presenter: PersoonPresenter = Depends(get_persoon_presenter),
):
    return presenter.present(existing_persoon, current_user)
