# structure-doc
# services = business logic
from .base import CommonService
from .organisatie import OrganisatieService
from .persoon import PersoonService

__all__ = [
    "CommonService",
    "OrganisatieService",
    "PersoonService"
]