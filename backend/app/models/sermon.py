from datetime import datetime

from app.extensions import db


class Sermon(db.Model):
    __tablename__ = "sermons"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    topic = db.Column(db.String(180), nullable=False)
    scripture = db.Column(db.String(180), nullable=True)
    outline = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "topic": self.topic,
            "scripture": self.scripture,
            "outline": self.outline,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
