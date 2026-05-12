from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class AIStatusResource(Resource):
    @jwt_required()
    def get(self):
        configured = bool(current_app.config["OPENAI_API_KEY"])
        return {
            "configured": configured,
            "model": current_app.config["OPENAI_MODEL"],
            "message": "AI is connected" if configured else "Add OPENAI_API_KEY to enable live AI responses",
        }
