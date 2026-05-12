from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models import Sermon
from app.services.ai_service import AIService
from app.utils.auth import current_user, minimum_role_required


class SermonListResource(Resource):
    @jwt_required()
    def get(self):
        sermons = Sermon.query.order_by(Sermon.created_at.desc()).all()
        return {"sermons": [sermon.to_dict() for sermon in sermons]}

    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        user = current_user()
        sermon = Sermon(
            user_id=user.id,
            title=data.get("title") or data.get("topic") or "Untitled sermon",
            topic=data.get("topic", ""),
            scripture=data.get("scripture"),
            outline=data.get("outline"),
            content=data.get("content"),
            status=data.get("status", "draft"),
        )
        db.session.add(sermon)
        db.session.commit()
        return {"sermon": sermon.to_dict()}, 201


class SermonResource(Resource):
    @jwt_required()
    def get(self, sermon_id):
        sermon = Sermon.query.get_or_404(sermon_id)
        return {"sermon": sermon.to_dict()}

    @minimum_role_required("leader")
    def patch(self, sermon_id):
        sermon = Sermon.query.get_or_404(sermon_id)
        data = request.get_json() or {}
        for field in ["title", "topic", "scripture", "outline", "content", "status"]:
            if field in data:
                setattr(sermon, field, data[field])
        db.session.commit()
        return {"sermon": sermon.to_dict()}

    @minimum_role_required("leader")
    def delete(self, sermon_id):
        sermon = Sermon.query.get_or_404(sermon_id)
        db.session.delete(sermon)
        db.session.commit()
        return {"message": "Sermon deleted"}


class SermonGenerateResource(Resource):
    @minimum_role_required("leader")
    def post(self):
        data = request.get_json() or {}
        topic = data.get("topic", "").strip()
        mode = data.get("mode", "outline")
        if not topic:
            return {"message": "Topic is required"}, 400

        generated = AIService().generate_sermon(topic, data.get("scripture"), mode)
        if data.get("save"):
            user = current_user()
            sermon = Sermon(
                user_id=user.id,
                title=data.get("title") or topic,
                topic=topic,
                scripture=data.get("scripture"),
                outline=generated if mode == "outline" else None,
                content=generated if mode == "full" else None,
            )
            db.session.add(sermon)
            db.session.commit()
            return {"generated": generated, "sermon": sermon.to_dict()}, 201

        return {"generated": generated}
