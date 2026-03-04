# login, jwt, get_current_user
from typing import Annotated

from fastapi import Header


from pydantic import BaseModel


class CurrentUser(BaseModel):
    sub: str
    username: str
    scopes: list[str]
    authenticated: bool


async def get_current_user(
    x_user_role: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    scopes = []
    if x_user_role == "aangemeld":
        scopes = ["me"]
    if x_user_role == "admin":
        scopes = [
            "me",
            "personen:read",
            "personen:read-basic",
            "personen:write",
            "organisaties:read",
            "organisaties:write",
        ]
    elif x_user_role == "basic":
        scopes = ["me", "personen:read-basic"]
    if x_user_role in ("admin", "basic", "aangemeld"):
        return CurrentUser(sub="demo_user_id", username="demo_user", scopes=scopes, authenticated=True)
    return CurrentUser(
        sub="anoniem", username="anoniem", scopes=[], authenticated=False
    )  # unauthenticated users
