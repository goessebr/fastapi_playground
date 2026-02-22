# export common schema classes for easier imports
from .common import SystemFields
from .organisatie import OrganisatieBase, OrganisatieCreate, OrganisatieRef, OrganisatieResponse
from .persoon import PersoonBase, PersoonCreate, PersoonResponse

__all__ = [
    "SystemFields",
    "OrganisatieBase",
    "OrganisatieCreate",
    "OrganisatieRef",
    "OrganisatieResponse",
    "PersoonBase",
    "PersoonCreate",
    "PersoonResponse",
]

