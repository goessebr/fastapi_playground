from app.data.db.models import Organisatie
from app.exceptions.organisatie import OrganisatieUnauthenticatedException
from app.exceptions.organisatie import OrganisatiePermissionDenied
from app.security.auth import CurrentUser
from app.security.base import PoliciesBase


class OrganisatiePolicies(PoliciesBase):
    async def _can_view(self, organisatie: Organisatie, user: CurrentUser) -> bool:
        return "organisaties:read" in user.scopes

    async def _can_create(self, organisatie: Organisatie, user: CurrentUser) -> bool:
        return "organisaties:write" in user.scopes

    async def assert_view_access(self, organisatie: Organisatie, user: CurrentUser):
        if True: # organisatie.status.id > 50: Voor iedereen zichtbaar
            return
        if not user.authenticated:
            raise OrganisatieUnauthenticatedException
        if not self._can_view(organisatie, user):
            raise OrganisatiePermissionDenied

    async def assert_create_access(self, organisatie: Organisatie, user: CurrentUser):
        if not user.authenticated:
            raise OrganisatieUnauthenticatedException
        if not self._can_create(organisatie, user):
            raise OrganisatiePermissionDenied