import requests
from django.conf import settings


class EmailService:

    @staticmethod
    def send(to_email, subject, body):
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        }

        payload = {
            "sender": {
                "email": settings.BREVO_FROM_EMAIL,
            },
            "to": [
                {
                    "email": to_email,
                }
            ],
            "subject": subject,
            "textContent": body,
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