from functools import wraps
from flask import request
from app.utils.response import error, unauthorized


def safe_route(func):
    """Decorator to catch exceptions in route handlers and return a JSON error."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # avoid exposing internal trace in production; include message for debugging
            return error(f"Internal server error: {str(e)}", status=500)

    return wrapper


def require_user(func):
    """Decorator to ensure request.user_id is present (set by auth before_request)."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = getattr(request, 'user_id', None)
        if user_id is None:
            return unauthorized("Missing or invalid authentication token")
        return func(*args, **kwargs)

    return wrapper
