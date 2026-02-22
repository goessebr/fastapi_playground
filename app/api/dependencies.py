from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.data.db.dao.persoon import PersoonDAO
from app.data.db.session import get_db as _get_db
from app.services import CommonService
from app.services import PersoonService
from app.services import OrganisatieService

# Organisatie imports
from app.data.db.dao.organisatie import OrganisatieDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


get_db = _get_db # Re-export the data-layer dependency for API use.


def get_settings_dep():
    """Dependency that returns the cached Settings instance."""
    return get_settings()


async def get_current_user() -> dict:
    return {
        "username": "demo_user",
        "scopes": ["me", "items"],
    }

# async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
#     """Very small placeholder dependency that decodes a JWT and returns the token payload.
#
#     Replace with a real user lookup in your application.
#     """
#     payload = decode_access_token(token)
#     if not payload:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     return payload



def get_persoon_repository(db: AsyncSession = Depends(get_db)) -> PersoonDAO:
    return PersoonDAO(db)

# Organisatie dependency factories
def get_organisatie_repository(db: AsyncSession = Depends(get_db)) -> OrganisatieDAO:
    return OrganisatieDAO(db)

def get_common_service() -> CommonService:
    return CommonService()

def get_persoon_service(common: CommonService = Depends(get_common_service), repo: PersoonDAO = Depends(get_persoon_repository), org_repo: OrganisatieDAO = Depends(get_organisatie_repository)) -> PersoonService:
    return PersoonService(common, repo, org_repo)

def get_organisatie_service(common: CommonService = Depends(get_common_service), repo: OrganisatieDAO = Depends(get_organisatie_repository)) -> OrganisatieService:
    return OrganisatieService(common, repo)
