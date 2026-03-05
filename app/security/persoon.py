from app.data.db.models import Persoon
from app.enums import ZichtbaarheidEnum
from app.exceptions.persoon import PersoonUnauthenticatedException
from app.exceptions.persoon import PersoonPermissionDenied
from app.security.auth import CurrentUser
from app.security.base import PoliciesBase


class PersoonPolicies(PoliciesBase):
    async def _can_view(self, persoon: Persoon, user: CurrentUser) -> bool:
        if persoon.zichtbaarheid == ZichtbaarheidEnum.publiek:
            return True
        return "personen:read-basic" in user.scopes

    async def _can_update(self, persoon: Persoon, user: CurrentUser) -> bool:
        # if persoon.dataverantwoordelijke != user.dataverantwoordelijke:
        #     return False
        return "personen:write" in user.scopes

    async def _can_create(self, user: CurrentUser) -> bool:
        # if persoon.dataverantwoordelijke != user.dataverantwoordelijke:
        #     return False
        return "personen:write" in user.scopes

    async def assert_view_access(self, persoon: Persoon, user: CurrentUser):
        if not user.authenticated:
            raise PersoonUnauthenticatedException
        if not self._can_view(persoon, user):
            raise PersoonPermissionDenied

    async def assert_update_access(self, persoon: Persoon, user: CurrentUser):
        if not user.authenticated:
            raise PersoonUnauthenticatedException
        if not self._can_update(persoon, user):
            raise PersoonPermissionDenied

    async def assert_create_access(self, user: CurrentUser):
        if not user.authenticated:
            raise PersoonUnauthenticatedException
        if not self._can_create(user):
            raise PersoonPermissionDenied
