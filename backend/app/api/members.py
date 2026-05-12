from datetime import date

from flask import request
from flask_restful import Resource

from app.extensions import db
from app.models import Member
from app.utils.auth import minimum_role_required


class MemberListResource(Resource):
    @minimum_role_required("leader")
    def get(self):
        members = Member.query.order_by(Member.last_name.asc(), Member.first_name.asc()).all()
        return {"members": [member.to_dict() for member in members]}

    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        member = Member(
            user_id=data.get("user_id"),
            first_name=data.get("first_name", "").strip(),
            last_name=data.get("last_name", "").strip(),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            ministry=data.get("ministry"),
            group_name=data.get("group_name"),
            status=data.get("status", "active"),
        )
        if data.get("joined_at"):
            member.joined_at = date.fromisoformat(data["joined_at"])
        if not member.first_name or not member.last_name:
            return {"message": "First name and last name are required"}, 400
        db.session.add(member)
        db.session.commit()
        return {"member": member.to_dict()}, 201


class MemberResource(Resource):
    @minimum_role_required("leader")
    def get(self, member_id):
        member = Member.query.get_or_404(member_id)
        return {"member": member.to_dict()}

    @minimum_role_required("leader")
    def patch(self, member_id):
        member = Member.query.get_or_404(member_id)
        data = request.get_json() or {}
        for field in [
            "user_id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "address",
            "ministry",
            "group_name",
            "status",
        ]:
            if field in data:
                setattr(member, field, data[field])
        if data.get("joined_at"):
            member.joined_at = date.fromisoformat(data["joined_at"])
        db.session.commit()
        return {"member": member.to_dict()}

    @minimum_role_required("admin")
    def delete(self, member_id):
        member = Member.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return {"message": "Member deleted"}
