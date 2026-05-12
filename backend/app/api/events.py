from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models import Event
from app.utils.auth import current_user, minimum_role_required
from app.utils.parsing import parse_iso_datetime


class EventListResource(Resource):
    @jwt_required()
    def get(self):
        events = Event.query.order_by(Event.starts_at.asc()).all()
        return {"events": [event.to_dict() for event in events]}

    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        try:
            starts_at = parse_iso_datetime(data.get("starts_at"), "starts_at")
            ends_at = parse_iso_datetime(data["ends_at"], "ends_at") if data.get("ends_at") else None
        except ValueError as exc:
            return {"message": str(exc)}, 400

        user = current_user()
        event = Event(
            title=data.get("title", "").strip(),
            description=data.get("description"),
            location=data.get("location"),
            starts_at=starts_at,
            ends_at=ends_at,
            created_by=user.id,
        )
        if not event.title:
            return {"message": "Title is required"}, 400
        db.session.add(event)
        db.session.commit()
        return {"event": event.to_dict()}, 201


class EventResource(Resource):
    @jwt_required()
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return {"event": event.to_dict()}

    @minimum_role_required("leader")
    def patch(self, event_id):
        event = Event.query.get_or_404(event_id)
        data = request.get_json() or {}
        for field in ["title", "description", "location"]:
            if field in data:
                setattr(event, field, data[field])
        try:
            if data.get("starts_at"):
                event.starts_at = parse_iso_datetime(data["starts_at"], "starts_at")
            if data.get("ends_at"):
                event.ends_at = parse_iso_datetime(data["ends_at"], "ends_at")
        except ValueError as exc:
            return {"message": str(exc)}, 400
        db.session.commit()
        return {"event": event.to_dict()}

    @minimum_role_required("leader")
    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}
