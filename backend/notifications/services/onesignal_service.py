import requests
from django.conf import settings


class OneSignalService:
    @staticmethod
    def send(subscription_id, title, body):
        url = "https://api.onesignal.com/notifications"

        headers = {
            "Authorization": f"Key {settings.ONESIGNAL_REST_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "app_id": settings.ONESIGNAL_APP_ID,
            "include_subscription_ids": [subscription_id],
            "headings": {
                "en": title or "Notification",
            },
            "contents": {
                "en": body,
            },
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