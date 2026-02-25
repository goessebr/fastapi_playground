# login, jwt, get_current_user

async def get_current_user() -> dict:
    if True:  # TODO: implement real authentication
        return {
            "username": "demo_user",
            "scopes": ["me", "personen:read", "personen:read-basic", "personen:write", "organisaties:read", "organisaties:write"],
            # "scopes": ["me", "personen:read-basic"], # simulate a user with basic permissions
            # "scopes": [],  # simulate a user with no permissions
        }
    return {}  # Return an empty dict for unauthenticated users
