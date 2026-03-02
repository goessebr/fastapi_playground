from app.enums import ZichtbaarheidEnum
from app.schemas import PersoonResponse
from app.schemas.persoon import PersoonResponseAnoniem
from app.schemas.persoon import PersoonResponseFull


class PersoonPresenter:
    def present(self, persoon: PersoonResponse, user: dict) -> type[PersoonResponse]:
        """
        Valideer en presenteer de persoon in het juiste schema, obv van rechten van de gebruiker
        :param persoon:
        :param user:
        :return:
        """
        if persoon.zichtbaarheid == ZichtbaarheidEnum.publiek:
            return PersoonResponseFull.model_validate(persoon)
        if user.get("scopes") and "personen:read" in user.get("scopes"):
            return PersoonResponseFull.model_validate(persoon)
        return PersoonResponseAnoniem.model_validate(persoon)

