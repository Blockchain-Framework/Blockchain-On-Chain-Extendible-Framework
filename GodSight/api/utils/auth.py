from flask import request, abort
from functools import wraps

_secret_api_key = None


def set_api_key(key):
    global _secret_api_key
    if _secret_api_key is not None:
        raise ValueError("API key has already been set and cannot be changed.")
    _secret_api_key = key


def get_secret_api_key():
    """Access function to get the secret API key."""
    return _secret_api_key


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if api_key != get_secret_api_key():
            abort(401, description="Invalid or missing API key.")
        return f(*args, **kwargs)

    return decorated_function
