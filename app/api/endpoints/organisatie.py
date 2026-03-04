from fastapi import HTTPException, APIRouter, Depends, status

from app.api.dependencies import get_current_user
from app.api.dependencies import get_organisatie_service
from app.api.endpoints.auth import CurrentUserDependency
from app.api.endpoints.fastapi_oeutils import assert_resource_exists
from app.exceptions.organisatie import EXC_MSG_ORGANISATIE_NOT_FOUND
from app.exceptions.organisatie import OrganisatieExistsException
from app.schemas.organisatie import OrganisatieCreate, OrganisatieResponse
from app.security.auth import CurrentUser
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
)
async def get_organisatie(
    organisatie_id: int, service: OrganisatieService = Depends(get_organisatie_service)
):
    organisatie = await service.get_organisatie(organisatie_id)
    assert_resource_exists(organisatie, msg_404=EXC_MSG_ORGANISATIE_NOT_FOUND)
    return organisatie
