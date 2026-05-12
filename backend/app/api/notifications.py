from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.models import Notification
from app.services.notification_service import NotificationService
from app.utils.auth import minimum_role_required


class NotificationListResource(Resource):
    @jwt_required()
    def get(self):
        notifications = Notification.query.order_by(Notification.created_at.desc()).limit(100).all()
        return {"notifications": [notification.to_dict() for notification in notifications]}


class SendNotificationResource(Resource):
    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        required = ["channel", "recipient", "subject", "body"]
        missing = [field for field in required if not data.get(field)]
        if missing:
            return {"message": f"Missing fields: {', '.join(missing)}"}, 400
        notification = NotificationService().send(
            data["channel"],
            data["recipient"],
            data["subject"],
            data["body"],
            user_id=data.get("user_id"),
            member_id=data.get("member_id"),
        )
        return {"notification": notification.to_dict()}, 201
