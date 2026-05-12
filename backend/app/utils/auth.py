from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import User

ROLE_HIERARCHY = {
    "member": 1,
    "leader": 2,
    "pastor": 3,
    "admin": 4,
}


def current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(int(user_id))


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user or not user.is_active:
                return {"message": "Unauthorized"}, 401
            if user.role not in roles:
                return {"message": "Forbidden"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def minimum_role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user or not user.is_active:
                return {"message": "Unauthorized"}, 401
            if ROLE_HIERARCHY.get(user.role, 0) < ROLE_HIERARCHY.get(role, 0):
                return {"message": "Forbidden"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
