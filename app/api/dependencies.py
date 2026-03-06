from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.data.db.dao.persoon import PersoonDAO
from app.data.db.models import Organisatie
from app.data.db.models import Persoon
from app.data.db.session import get_db as _get_db
from app.exceptions.organisatie import OrganisatieNotFoundException
from app.exceptions.persoon import PersoonNotFoundException
from app.presenters.persoon import PersoonPresenter
from app.security import OrganisatiePolicies
from app.security import PersoonPolicies
from app.security.auth import CurrentUser
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
get_db = _get_db  # Re-export the data-layer dependency for API use.
get_current_user = _get_current_user  # Re-export the auth dependency for API use.
CurrentUserDependency = Annotated[
    CurrentUser, Depends(get_current_user)
]  # Type-alias for cleaner annotations


def get_settings_dep():
    """Dependency that returns the cached Settings instance."""
    return get_settings()


def get_common_service() -> CommonService:
    return CommonService()


##########################################
### Organisatie dependencies           ###
##########################################
def get_organisatie_repository(db: AsyncSession = Depends(get_db)) -> OrganisatieDAO:
    return OrganisatieDAO(db)


def get_organisatie_service(
    common: CommonService = Depends(get_common_service),
    repo: OrganisatieDAO = Depends(get_organisatie_repository),
) -> OrganisatieService:
    return OrganisatieService(common, repo)


async def get_existing_organisatie(
    organisatie_id: int,  # Param
    service: OrganisatieService = Depends(get_organisatie_service),
) -> Organisatie:
    organisatie = await service.get_organisatie(organisatie_id)
    if organisatie is None:
        raise OrganisatieNotFoundException
    return organisatie


ExistingOrganisatieDependency = Annotated[
    Organisatie, Depends(get_existing_organisatie)
]  # Type-alias for cleaner annotations


def get_organisatie_policy() -> OrganisatiePolicies:
    return OrganisatiePolicies()


async def assert_organisatie_view_access(
    current_user: CurrentUserDependency,
    organisatie: ExistingOrganisatieDependency,
    policy: OrganisatiePolicies = Depends(get_organisatie_policy),
) -> None:
    await policy.assert_view_access(organisatie=organisatie, user=current_user)


async def assert_organisatie_update_access(
    current_user: CurrentUserDependency,
    organisatie: ExistingOrganisatieDependency,
    policy: OrganisatiePolicies = Depends(get_organisatie_policy),
) -> None:
    await policy.assert_update_access(organisatie=organisatie, user=current_user)


async def assert_organisatie_create_access(
    current_user: CurrentUserDependency,
    policy: OrganisatiePolicies = Depends(get_organisatie_policy),
) -> None:
    await policy.assert_create_access(user=current_user)


def get_persoon_repository(db: AsyncSession = Depends(get_db)) -> PersoonDAO:
    return PersoonDAO(db)


def get_persoon_service(
    common: CommonService = Depends(get_common_service),
    repo: PersoonDAO = Depends(get_persoon_repository),
    org_repo: OrganisatieDAO = Depends(get_organisatie_repository),
) -> PersoonService:
    return PersoonService(common, repo, org_repo)


def get_persoon_presenter() -> PersoonPresenter:
    return persoon_presenter


async def get_existing_persoon(
    persoon_id: int,  # Param
    service: PersoonService = Depends(get_persoon_service),
) -> Persoon:
    persoon = await service.get_persoon(persoon_id)
    if persoon is None:
        raise PersoonNotFoundException
    return persoon


ExistingPersoonDependency = Annotated[
    Persoon, Depends(get_existing_persoon)
]  # Type-alias for cleaner annotations


def get_persoon_policy() -> PersoonPolicies:
    return PersoonPolicies()


async def assert_persoon_view_access(
    current_user: CurrentUserDependency,
    persoon: ExistingPersoonDependency,
    policy: PersoonPolicies = Depends(get_persoon_policy),
) -> None:
    await policy.assert_view_access(persoon=persoon, user=current_user)


async def assert_persoon_create_access(
    current_user: CurrentUserDependency,
    policy: PersoonPolicies = Depends(get_persoon_policy),
) -> None:
    await policy.assert_create_access(user=current_user)


async def assert_persoon_update_access(
    current_user: CurrentUserDependency,
    persoon: ExistingPersoonDependency,
    policy: PersoonPolicies = Depends(get_persoon_policy),
) -> None:
    await policy.assert_update_access(persoon=persoon, user=current_user)
