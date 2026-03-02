# login, jwt, get_current_user
from typing import Annotated

from fastapi import Header


async def get_current_user(x_user_role: Annotated[str | None, Header()] = None) -> dict:
    scopes = []
    if x_user_role == "aangemeld":
        scopes = ["me"]
    if x_user_role == "admin":
        scopes = ["me", "personen:read", "personen:read-basic", "personen:write", "organisaties:read", "organisaties:write"]
    elif x_user_role == "basic":
        scopes = ["me", "personen:read-basic"]
    if x_user_role in ("admin", "basic", "aangemeld"):
        return {
            "username": "demo_user",
            "scopes": scopes
        }
    return {}  # Return an empty dict for unauthenticated users
