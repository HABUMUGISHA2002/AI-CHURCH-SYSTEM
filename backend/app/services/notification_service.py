from datetime import datetime

import requests
from flask import current_app

from app.extensions import db
from app.models import Notification


class NotificationService:
    def send(self, channel, recipient, subject, body, user_id=None, member_id=None):
        notification = Notification(
            user_id=user_id,
            member_id=member_id,
            channel=channel,
            recipient=recipient,
            subject=subject,
            body=body,
            status="queued",
        )
        db.session.add(notification)
        db.session.flush()

        try:
            provider_id = self._dispatch(channel, recipient, subject, body)
            notification.status = "sent"
            notification.provider_message_id = provider_id
            notification.sent_at = datetime.utcnow()
        except Exception as exc:
            notification.status = "failed"
            notification.provider_message_id = str(exc)[:120]

        db.session.commit()
        return notification

    def _dispatch(self, channel, recipient, subject, body):
        if channel == "email":
            return self._send_email(recipient, subject, body)
        if channel == "sms":
            return self._send_sms(recipient, body)
        if channel == "whatsapp":
            return self._send_whatsapp(recipient, body)
        raise ValueError("Unsupported notification channel")

    def _send_email(self, recipient, subject, body):
        # Real SMTP sending can be added here without changing routes.
        if not current_app.config["SMTP_HOST"]:
            return "email-provider-not-configured"
        return f"email:{recipient}:{subject}"

    def _send_sms(self, recipient, body):
        base_url = current_app.config["SMS_PROVIDER_BASE_URL"]
        api_key = current_app.config["SMS_PROVIDER_API_KEY"]
        if not base_url or not api_key:
            return "sms-provider-not-configured"
        response = requests.post(
            base_url,
            json={"to": recipient, "message": body},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("id", "sms-sent")

    def _send_whatsapp(self, recipient, body):
        token = current_app.config["WHATSAPP_ACCESS_TOKEN"]
        phone_id = current_app.config["WHATSAPP_PHONE_NUMBER_ID"]
        if not token or not phone_id:
            return "whatsapp-provider-not-configured"
        response = requests.post(
            f"https://graph.facebook.com/v19.0/{phone_id}/messages",
            json={
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "text",
                "text": {"body": body},
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("messages", [{}])[0].get("id", "whatsapp-sent")
