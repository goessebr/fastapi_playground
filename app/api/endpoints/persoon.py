from fastapi import HTTPException

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.api.dependencies import get_current_user
from app.exceptions.persoon import PersoonExistsException
from app.schemas.persoon import PersoonCreate
from app.schemas.persoon import PersoonResponse
from app.services.persoon_service import PersoonService
from app.api.dependencies import get_persoon_service

from app.core.logging import get_logger

LOG = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=PersoonResponse, status_code=status.HTTP_201_CREATED,
             responses={
                 400: {
                     "description": "Persoon bestaat reeds",
                     "content": {
                         "application/json": {
                             "example": {"detail": "Persoon bestaat reeds"}
                         }
                     }
                 }
             },
             )
async def create_persoon(persoon_data: PersoonCreate,
                         service: PersoonService = Depends(get_persoon_service),
                         current_user: dict = Depends(get_current_user),):
    try:
        created = await service.create_persoon(persoon_data, created_by=current_user)
    except PersoonExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Persoon bestaat reeds",
        )
    return created

@router.get("/{persoon_id}", response_model=PersoonResponse,
            responses={
                404: {
                    "description": "Persoon niet gevonden",
                    "content": {
                        "application/json": {
                            "example": {"detail": "Persoon niet gevonden"}
                        }
                    }
                }
            },
            )
async def get_persoon(persoon_id: int, service: PersoonService = Depends(get_persoon_service)):
    persoon = await service.get_persoon(persoon_id)
    if not persoon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persoon niet gevonden")
    return persoon