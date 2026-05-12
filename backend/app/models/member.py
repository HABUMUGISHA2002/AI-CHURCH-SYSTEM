from datetime import datetime

from app.extensions import db


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    ministry = db.Column(db.String(120), nullable=True)
    group_name = db.Column(db.String(120), nullable=True)
    joined_at = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="member")
    attendance_records = db.relationship("Attendance", back_populates="member", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": f"{self.first_name} {self.last_name}",
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "ministry": self.ministry,
            "group_name": self.group_name,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
