from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from app.api.dependencies import get_current_user

router = APIRouter()

CurrentUserDependency = Annotated[dict, Depends(get_current_user)]
