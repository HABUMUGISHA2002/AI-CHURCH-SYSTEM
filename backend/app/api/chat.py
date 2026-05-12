from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models import Message
from app.services.ai_service import AIService
from app.utils.auth import current_user


class BibleQuestionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        question = data.get("question", "").strip()
        if not question:
            return {"message": "Question is required"}, 400

        answer = AIService().answer_bible_question(question)
        user = current_user()
        message = Message(user_id=user.id, channel="web", direction="inbound", question=question, response=answer)
        db.session.add(message)
        db.session.commit()
        return {"message": message.to_dict()}, 201


class ChatHistoryResource(Resource):
    @jwt_required()
    def get(self):
        user = current_user()
        messages = (
            Message.query.filter_by(user_id=user.id)
            .order_by(Message.created_at.desc())
            .limit(50)
            .all()
        )
        return {"messages": [message.to_dict() for message in messages]}
