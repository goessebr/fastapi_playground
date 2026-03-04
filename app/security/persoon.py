from app.data.db.models import Persoon
from app.enums import ZichtbaarheidEnum
from app.exceptions.persoon import PersoonUnauthenticatedException
from app.exceptions.persoon import PersoonPermissionDenied
from app.security.auth import CurrentUser
from app.security.base import PoliciesBase


class PersoonPolicies(PoliciesBase):
    def _can_view(self, persoon: Persoon, user: CurrentUser) -> CurrentUser:
        if persoon.zichtbaarheid == ZichtbaarheidEnum.publiek:
            return True
        return "personen:read-basic" in user.scopes

    def _can_edit(self, persoon: Persoon, user: CurrentUser) -> CurrentUser:
        # if persoon.dataverantwoordelijke != user["dataverantwoordelijke"]:
        #     return False
        return "personen:edit" in user.scopes

    def assert_view_access(self, persoon: Persoon, user: CurrentUser):
        if user.username is None:
            raise PersoonUnauthenticatedException
        if not self._can_view(persoon, user):
            raise PersoonPermissionDenied

    def assert_edit_access(self, persoon: Persoon, user: CurrentUser):
        if user.username is None:
            raise PersoonUnauthenticatedException
        if not self._can_edit(persoon, user):
            raise PersoonPermissionDenied
