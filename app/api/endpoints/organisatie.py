from fastapi import HTTPException, APIRouter, Depends, status

from app.api.dependencies import CurrentUserDependency
from app.api.dependencies import ExistingOrganisatieDependency
from app.api.dependencies import assert_organisatie_create_access
from app.api.dependencies import assert_organisatie_view_access
from app.api.dependencies import get_organisatie_service
from app.exceptions.organisatie import OrganisatieExistsException
from app.schemas.organisatie import OrganisatieCreate, OrganisatieResponse
from app.services.organisatie import OrganisatieService

from app.core.logging import get_logger
from app.api.responses import RESPONSES_GET_ORGANISATIE
from app.api.responses import RESPONSES_POST_ORGANISATIE

LOG = get_logger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=OrganisatieResponse,
    status_code=status.HTTP_201_CREATED,
    responses=RESPONSES_POST_ORGANISATIE,
    dependencies=[Depends(assert_organisatie_create_access)],
)
async def create_organisatie(
    organisatie_data: OrganisatieCreate,
    current_user: CurrentUserDependency,
    service: OrganisatieService = Depends(get_organisatie_service),
):
    try:
        created = await service.create_organisatie(
            organisatie_data, created_by=current_user
        )
    except OrganisatieExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisatie bestaat reeds",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return created


@router.get(
    "/{organisatie_id}",
    response_model=OrganisatieResponse,
    responses=RESPONSES_GET_ORGANISATIE,
    dependencies=[Depends(assert_organisatie_view_access)],
)
async def get_organisatie(
    existing_organisatie: ExistingOrganisatieDependency,
):
    return existing_organisatie
