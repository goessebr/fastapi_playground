from app.data.db.models import Organisatie
from app.exceptions.organisatie import OrganisatieUnauthenticatedException
from app.exceptions.organisatie import OrganisatiePermissionDenied
from app.security.base import PoliciesBase


class OrganisatiePolicies(PoliciesBase):
    def _can_view(self, organisatie: Organisatie, user: dict) -> bool:
        return "organisaties:read" in user.get("scopes")

    def _can_edit(self, organisatie: Organisatie, user: dict) -> bool:
        return "organisaties:edit" in user.get("scopes")

    def assert_view_access(self, organisatie: Organisatie, user: dict):
        if user.get("username") is None:
            raise OrganisatieUnauthenticatedException
        if not self._can_view(organisatie, user):
            raise OrganisatiePermissionDenied

    def assert_edit_access(self, organisatie: Organisatie, user: dict):
        if user.get("username") is None:
            raise OrganisatieUnauthenticatedException
        if not self._can_edit(organisatie, user):
            raise OrganisatiePermissionDenied
