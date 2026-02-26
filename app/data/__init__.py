# top-level data package re-exports
from .db import Base, get_db

__all__ = [
    "Base",
    "get_db",
]

