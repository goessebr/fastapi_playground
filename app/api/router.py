from fastapi import APIRouter

# endpoints
from app.api.endpoints import health
from app.api.endpoints import auth
from app.api.endpoints import persoon
from app.api.endpoints import organisatie

api_router = APIRouter()

api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(persoon.router, prefix="/personen", tags=["personen"])
api_router.include_router(organisatie.router, prefix="/organisaties", tags=["organisaties"])
