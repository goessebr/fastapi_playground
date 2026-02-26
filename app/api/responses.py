from app.exceptions.persoon import EXC_MSG_PERSOON_EXISTS
from app.exceptions.persoon import EXC_MSG_PERSOON_NOT_FOUND
from app.exceptions.persoon import EXC_MSG_PERSOON_PERMISSION_DENIED
from app.exceptions.persoon import EXC_MSG_PERSOON_UNAUTHENTICATED

RESPONSES_POST_PERSOON: dict = {
    400: {
        "description": "Validatiefout bij het aanmaken van persoon",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_EXISTS}}
        },
    }
}

RESPONSES_GET_PERSOON: dict = {
    401: {
        "description": "Niet geauthenticeerd",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_UNAUTHENTICATED}}
        },
    },
    403: {
        "description": "Geen toegang tot deze persoon",
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_PERMISSION_DENIED}}
        },
    },
    404: {
        "description": EXC_MSG_PERSOON_NOT_FOUND,
        "content": {
            "application/json": {"example": {"detail": EXC_MSG_PERSOON_NOT_FOUND}}
        },
    },
}