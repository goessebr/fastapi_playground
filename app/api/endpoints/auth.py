from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from app.api.dependencies import get_current_user
from app.security.auth import CurrentUser

router = APIRouter()

CurrentUserDependency = Annotated[CurrentUser, Depends(get_current_user)]
