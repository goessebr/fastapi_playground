from app.data.db.models import Persoon
from app.enums import ZichtbaarheidEnum
from app.exceptions.persoon import PersoonUnauthenticatedException
from app.exceptions.persoon import PersoonPermissionDenied


class PersoonPolicies:
    def _can_view(self, persoon: Persoon, user: dict) -> bool:
        return not (
            persoon.zichtbaarheid == ZichtbaarheidEnum.privaat
            and "personen:read-basic" not in user.get("scopes")
        )

    def assert_view(self, persoon: Persoon, user: dict):
        if persoon.zichtbaarheid == ZichtbaarheidEnum.publiek:
            return
        if user.get("username") is None:
            raise PersoonUnauthenticatedException
        if not self._can_view(persoon, user):
            raise PersoonPermissionDenied
