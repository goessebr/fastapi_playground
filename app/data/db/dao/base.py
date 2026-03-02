from abc import ABC


class BaseDAO(ABC):
    """
    Abstract base class for all Data Access Objects (DAOs).

    Serves purely as a shared parent type for type-hinting and DI/registry
    patterns. Intended to be subclassed; contains no concrete behavior.
    """
    pass