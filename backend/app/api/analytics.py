from flask_restful import Resource

from app.models import Attendance, Event, Member, Message, Notification, Sermon, User
from app.utils.auth import minimum_role_required


class AnalyticsResource(Resource):
    @minimum_role_required("leader")
    def get(self):
        return {
            "totals": {
                "users": User.query.count(),
                "members": Member.query.count(),
                "events": Event.query.count(),
                "attendance_records": Attendance.query.count(),
                "sermons": Sermon.query.count(),
                "messages": Message.query.count(),
                "notifications": Notification.query.count(),
            },
            "members_by_status": _count_by(Member, Member.status),
            "notifications_by_channel": _count_by(Notification, Notification.channel),
        }


def _count_by(model, column):
    rows = model.query.with_entities(column, model.id).all()
    counts = {}
    for value, _ in rows:
        counts[value or "unknown"] = counts.get(value or "unknown", 0) + 1
    return counts
