class UnauthenticatedException(Exception):
    """Raised when the user is not authenticated."""
    pass

class PermissionDenied(Exception):
    """Raised when the user does not have permission to perform an action."""
    pass
