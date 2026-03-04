from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.data.db.dao.persoon import PersoonDAO
from app.data.db.session import get_db as _get_db
from app.presenters.persoon import PersoonPresenter
from app.security.auth import get_current_user as _get_current_user
from app.services import CommonService
from app.services import PersoonService
from app.services import OrganisatieService

# Organisatie imports
from app.data.db.dao.organisatie import OrganisatieDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
persoon_presenter = PersoonPresenter()


##########################################
### General dependencies               ###
##########################################
get_db = _get_db # Re-export the data-layer dependency for API use.
get_current_user = _get_current_user # Re-export the auth dependency for API use.

def get_settings_dep():
    """Dependency that returns the cached Settings instance."""
    return get_settings()

def get_common_service() -> CommonService:
    return CommonService()

##########################################
### Persoon dependencies               ###
##########################################

def get_persoon_repository(db: AsyncSession = Depends(get_db)) -> PersoonDAO:
    return PersoonDAO(db)

def get_persoon_service(common: CommonService = Depends(get_common_service), repo: PersoonDAO = Depends(get_persoon_repository), org_repo: OrganisatieDAO = Depends(get_organisatie_repository)) -> PersoonService:
    return PersoonService(common, repo, org_repo)

def get_persoon_presenter() -> PersoonPresenter:
    return persoon_presenter

##########################################
### Organisatie dependencies           ###
##########################################
def get_organisatie_repository(db: AsyncSession = Depends(get_db)) -> OrganisatieDAO:
    return OrganisatieDAO(db)

def get_organisatie_service(common: CommonService = Depends(get_common_service), repo: OrganisatieDAO = Depends(get_organisatie_repository)) -> OrganisatieService:
    return OrganisatieService(common, repo)
