from abc import ABC
from abc import abstractmethod

from app.api.endpoints.fastapi_oeutils import AccessTypes
from app.data.db.base import Base as ORMBase


class PoliciesBase(ABC):
    @abstractmethod
    def assert_access(self, access_type: str, persoon: ORMBase, user: dict):
        pass