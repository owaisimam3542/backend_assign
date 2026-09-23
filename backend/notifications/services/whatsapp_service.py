import requests
from django.conf import settings


class WhatsAppService:

    @staticmethod
    def send(to_phone, message):
        url = (
            f"https://graph.facebook.com/v23.0/"
            f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )

        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {
                "body": message
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15,
        )

        if response.ok:
            return {
                "success": True,
                "response": response.json(),
            }

        return {
            "success": False,
            "response": response.text,
        }