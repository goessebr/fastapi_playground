from abc import ABC

from app.data.db.base import Base as ORMBase
from app.security.auth import CurrentUser


class PoliciesBase(ABC):
    def assert_view_access(self, baseobject: ORMBase, user: CurrentUser):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement assert_view_access method"
        )

    def assert_edit_access(self, baseobject: ORMBase, user: CurrentUser):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement assert_edit_access method"
        )
