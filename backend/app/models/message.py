from datetime import datetime

from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    channel = db.Column(db.String(30), nullable=False, default="web")
    direction = db.Column(db.String(20), nullable=False, default="inbound")
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    external_sender = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "channel": self.channel,
            "direction": self.direction,
            "question": self.question,
            "response": self.response,
            "external_sender": self.external_sender,
            "created_at": self.created_at.isoformat(),
        }
