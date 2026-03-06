from abc import ABC

from app.security.auth import CurrentUser
from app.security.base import PoliciesBase


class BaseService(ABC):
    policies: PoliciesBase


class CommonService:
    def set_system_fields_new_entry(self, model_dump: dict, created_by: CurrentUser) -> None:
        # model_dump.setdefault("created_by", created_by.username)  # voor later
        self.set_system_fields_existing_entry(
            model_dump=model_dump, updated_by=created_by
        )

    def set_system_fields_existing_entry(
        self, model_dump: dict, updated_by: CurrentUser
    ) -> None:
        model_dump.setdefault("updated_by", updated_by.username)
