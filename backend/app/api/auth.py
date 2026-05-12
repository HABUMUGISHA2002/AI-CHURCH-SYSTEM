from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models import User
from app.utils.auth import current_user, roles_required

ALLOWED_ROLES = {"admin", "pastor", "leader", "member"}


class RegisterResource(Resource):
    def post(self):
        data = request.get_json() or {}
        required = ["name", "email", "password"]
        missing = [field for field in required if not data.get(field)]
        if missing:
            return {"message": f"Missing fields: {', '.join(missing)}"}, 400

        if User.query.filter_by(email=data["email"].lower()).first():
            return {"message": "Email is already registered"}, 409

        role = data.get("role", "member")
        if role not in ALLOWED_ROLES:
            return {"message": "Invalid role"}, 400

        user = User(name=data["name"], email=data["email"].lower(), role=role)
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return {"user": user.to_dict(), "access_token": token}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(email=(data.get("email") or "").lower()).first()
        if not user or not user.check_password(data.get("password", "")):
            return {"message": "Invalid email or password"}, 401
        if not user.is_active:
            return {"message": "Account is disabled"}, 403

        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return {"user": user.to_dict(), "access_token": token}


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = current_user()
        if not user:
            return {"message": "Unauthorized"}, 401
        return {"user": user.to_dict()}

    @roles_required("admin")
    def patch(self):
        data = request.get_json() or {}
        user = User.query.get(data.get("user_id"))
        if not user:
            return {"message": "User not found"}, 404
        if data.get("role") in ALLOWED_ROLES:
            user.role = data["role"]
        if "is_active" in data:
            user.is_active = bool(data["is_active"])
        db.session.commit()
        return {"user": user.to_dict()}
