from datetime import datetime

from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=True)
    channel = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(180), nullable=False)
    body = db.Column(db.Text, nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="queued")
    provider_message_id = db.Column(db.String(120), nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")
    member = db.relationship("Member")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "member_id": self.member_id,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "recipient": self.recipient,
            "status": self.status,
            "provider_message_id": self.provider_message_id,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "created_at": self.created_at.isoformat(),
        }
