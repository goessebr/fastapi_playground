from fastapi import HTTPException, APIRouter, Depends, status

from app.api.dependencies import get_current_user
from app.api.dependencies import get_organisatie_service
from app.exceptions.organisatie import OrganisatieExistsException
from app.schemas.organisatie import OrganisatieCreate, OrganisatieResponse
from app.services.organisatie import OrganisatieService

from app.core.logging import get_logger

LOG = get_logger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=OrganisatieResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Validatiefout bij het aanmaken van organisatie",
            "content": {
                "application/json": {
                    "example": {"detail": "Organisatie bestaat reeds"}
                }
            },
        }
    },
)
async def create_organisatie(
    organisatie_data: OrganisatieCreate,
    service: OrganisatieService = Depends(get_organisatie_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        created = await service.create_organisatie(organisatie_data, created_by=current_user)
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
    responses={
        404: {
            "description": "Organisatie niet gevonden",
            "content": {
                "application/json": {
                    "example": {"detail": "Organisatie niet gevonden"}
                }
            },
        }
    },
)
async def get_organisatie(organisatie_id: int, service: OrganisatieService = Depends(get_organisatie_service)):
    organisatie = await service.get_organisatie(organisatie_id)
    if not organisatie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisatie niet gevonden")
    return organisatie