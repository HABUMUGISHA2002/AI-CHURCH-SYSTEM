from flask import current_app, request
from flask_restful import Resource

from app.extensions import db
from app.models import Message
from app.services.ai_service import AIService
from app.services.notification_service import NotificationService


class WhatsAppWebhookResource(Resource):
    def get(self):
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == current_app.config["WHATSAPP_VERIFY_TOKEN"]:
            return int(challenge), 200
        return {"message": "Verification failed"}, 403

    def post(self):
        payload = request.get_json() or {}
        inbound = _extract_message(payload)
        if not inbound:
            return {"status": "ignored"}, 200

        answer = AIService().answer_bible_question(inbound["text"])
        message = Message(
            channel="whatsapp",
            direction="inbound",
            question=inbound["text"],
            response=answer,
            external_sender=inbound["from"],
        )
        db.session.add(message)
        db.session.commit()

        NotificationService().send("whatsapp", inbound["from"], "Bible Q&A", answer)
        return {"status": "processed"}, 200


def _extract_message(payload):
    try:
        value = payload["entry"][0]["changes"][0]["value"]
        message = value["messages"][0]
        return {"from": message["from"], "text": message["text"]["body"]}
    except (KeyError, IndexError, TypeError):
        return None
