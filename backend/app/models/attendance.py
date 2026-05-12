from datetime import datetime

from app.extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="present")
    checked_in_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(255), nullable=True)

    event = db.relationship("Event", back_populates="attendance_records")
    member = db.relationship("Member", back_populates="attendance_records")

    __table_args__ = (db.UniqueConstraint("event_id", "member_id", name="uq_attendance_event_member"),)

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "member_id": self.member_id,
            "status": self.status,
            "checked_in_at": self.checked_in_at.isoformat(),
            "notes": self.notes,
            "member": self.member.to_dict() if self.member else None,
        }
