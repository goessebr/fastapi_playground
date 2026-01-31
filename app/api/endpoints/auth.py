from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.core.security import create_access_token
from app.core.security import verify_password
from app.core.security import get_password_hash
from app.api.dependencies import get_current_user

router = APIRouter()

# FAKE_USERS_DB = {
#     "alice": {"username": "alice", "password_hash": get_password_hash("secret")},
# }
#
#
# @router.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = FAKE_USERS_DB.get(form_data.username)
#     if not user or not verify_password(form_data.password, user["password_hash"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(subject=form_data.username, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @router.get("/me")
# async def read_users_me(current_user: dict = Depends(get_current_user)):
#     return {"user": current_user}

