from flask import request
from flask_restful import Resource

from app.extensions import db
from app.models import Attendance
from app.utils.auth import minimum_role_required


class AttendanceResource(Resource):
    @minimum_role_required("leader")
    def get(self):
        event_id = request.args.get("event_id")
        query = Attendance.query
        if event_id:
            query = query.filter_by(event_id=event_id)
        records = query.order_by(Attendance.checked_in_at.desc()).all()
        return {"attendance": [record.to_dict() for record in records]}

    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        if not data.get("event_id") or not data.get("member_id"):
            return {"message": "event_id and member_id are required"}, 400
        record = Attendance(
            event_id=data["event_id"],
            member_id=data["member_id"],
            status=data.get("status", "present"),
            notes=data.get("notes"),
        )
        db.session.add(record)
        db.session.commit()
        return {"attendance": record.to_dict()}, 201
