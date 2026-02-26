from app.api.endpoints.fastapi_oeutils import AccessTypes
from app.data.db.models import Persoon
from app.enums import ZichtbaarheidEnum
from app.exceptions.persoon import PersoonUnauthenticatedException
from app.exceptions.persoon import PersoonPermissionDenied
from app.security.base import PoliciesBase


class PersoonPolicies(PoliciesBase):
    def _can_view(self, persoon: Persoon, user: dict) -> bool:
        if persoon.zichtbaarheid == ZichtbaarheidEnum.publiek:
            return True
        return "personen:read-basic" in user.get("scopes")

    def _can_edit(self, persoon: Persoon, user: dict) -> bool:
        # if persoon.dataverantwoordelijke != user["dataverantwoordelijke"]:
        #     return False
        return "personen:edit" in user.get("scopes")

    def assert_access(self, access_type: str, persoon: Persoon, user: dict):
        if user.get("username") is None:
            raise PersoonUnauthenticatedException
        if access_type == AccessTypes.VIEW:
            if not self._can_view(persoon, user):
                raise PersoonPermissionDenied
        elif access_type == AccessTypes.EDIT:
            if not self._can_edit(persoon, user):
                raise PersoonPermissionDenied
