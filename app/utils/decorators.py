from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from ..models.user import User
from ..extensions import db


def jwt_required_and_get_user():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                user = db.session.get(User, user_id)
                if not user:
                    return {"message": "User not found"}, 404
                if not user.is_active:
                    return {"message": "Account is deactivated"}, 403
                return fn(user, *args, **kwargs)
            except Exception as e:
                return {"message": "Invalid token"}, 401
        return wrapper
    return decorator


def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                user = db.session.get(User, user_id)
                if not user:
                    return {"message": "User not found"}, 404
                if not user.is_active:
                    return {"message": "Account is deactivated"}, 403
                if user.role not in roles:
                    return {"message": "Insufficient permissions"}, 403
                return fn(user, *args, **kwargs)
            except Exception as e:
                return {"message": "Authorization failed"}, 401
        return wrapper
    return decorator


def handle_api_errors(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as e:
            return {"message": str(e)}, 400
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": "An internal error occurred"}, 500
    return wrapper
