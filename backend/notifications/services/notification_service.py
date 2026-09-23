import re
from .whatsapp_service import WhatsAppService
from django.contrib.auth.models import User
from .email_service import EmailService
from notifications.models import (
    NotificationLog,
    NotificationTemplate,
)


class NotificationService:

    @staticmethod
    def render_template(text, user):
        """
        Replace supported template variables with user data.
        """

        if not text:
            return ""

        variables = {
            "user_name": user.get_full_name() or user.username,
            "username": user.username,
            "email": user.email,
        }

        def replace_variable(match):
            variable = match.group(1).strip()
            return str(variables.get(variable, match.group(0)))

        return re.sub(
            r"\{\{\s*(.*?)\s*\}\}",
            replace_variable,
            text,
        )

    @classmethod
    def get_enabled_templates(cls, trigger):
        """
        Return all enabled templates for an active trigger.
        """

        if not trigger.is_active:
            return NotificationTemplate.objects.none()

        return NotificationTemplate.objects.filter(
            trigger=trigger,
            is_enabled=True,
        )

    @classmethod
    def prepare_notification(cls, template, user):
        """
        Render a notification template for a specific user.
        """

        return {
            "channel": template.channel,
            "title": cls.render_template(template.title, user),
            "subject": cls.render_template(template.subject, user),
            "body": cls.render_template(template.body, user),
        }

    @classmethod
    def create_log(
        cls,
        user,
        template,
        status,
        response="",
    ):
        """
        Store the result of a notification attempt.
        """

        return NotificationLog.objects.create(
            user=user,
            trigger=template.trigger,
            template=template,
            channel=template.channel,
            status=status,
            response=response,
        )

    @classmethod
    def dispatch(cls, trigger, user):
        templates = cls.get_enabled_templates(trigger)

        results = []

        for template in templates:
            notification = cls.prepare_notification(
                template,
                user,
            )

            if template.channel == "email":
                result = EmailService.send(
                    to_email=user.email,
                    subject=notification["subject"],
                    body=notification["body"],
                )

                if result["success"]:
                    cls.create_log(
                        user=user,
                        template=template,
                        status="success",
                        response=str(result["response"]),
                    )

                else:
                    cls.create_log(
                        user=user,
                        template=template,
                        status="failed",
                        response=str(result["response"]),
                    )

                notification["result"] = result
            elif template.channel == "whatsapp":
                phone_number = getattr(
                    getattr(user, "profile", None),
                    "phone_number",
                    None,
                )

                if not phone_number:
                    result = {
                        "success": False,
                        "response": "User does not have a WhatsApp phone number.",
                    }
                else:
                    result = WhatsAppService.send(
                        to_phone=phone_number,
                        message=notification["body"],
                    )

                status = "success" if result.get("success") else "failed"
                response = str(result.get("response", ""))

                cls.create_log(
                    user,
                    template,
                    status,
                    response,
                )
            elif template.channel == "web_push":
                from .onesignal_service import OneSignalService
                from notifications.models import PushSubscription

                subscription = PushSubscription.objects.filter(
                    user=user
                ).first()

                if not subscription:
                    result = {
                        "success": False,
                        "response": "User does not have a Web Push subscription.",
                    }
                else:
                    result = OneSignalService.send(
                        subscription_id=subscription.subscription_id,
                        title=notification["title"],
                        body=notification["body"],
                    )

                status = "success" if result.get("success") else "failed"
                response = str(result.get("response", ""))

                cls.create_log(
                    user,
                    template,
                    status,
                    response,
                )
                notification["result"] = result
            # elif template.channel == "whatsapp":
            #     result = WhatsAppService.send(
            #         to_phone=user.username,
            #         message=notification["body"],
            #     )
            #
            #     status = "success" if result.get("success") else "failed"
            #     response = str(result.get("response", ""))
            #
            #     cls.create_log(
            #         user,
            #         template,
            #         status,
            #         response,
            #     )
            #
            #     notification["result"] = result

            results.append(notification)

        return results