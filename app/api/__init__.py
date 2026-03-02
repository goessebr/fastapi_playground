"""API package: expose router and helper response maps."""
from .router import api_router
from . import responses

__all__ = ["api_router", "responses"]

# structure-doc
# api = transport/presentation