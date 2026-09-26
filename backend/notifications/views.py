from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .models import NotificationTemplate
from .services.notification_service import NotificationService
from .models import (
    Trigger,
    NotificationTemplate,
    PushSubscription,
    NotificationLog,
)
from .serializers import (
    TriggerSerializer,
    NotificationTemplateSerializer,
    PushSubscriptionSerializer,
    NotificationLogSerializer,
)


class TriggerListCreateView(generics.ListCreateAPIView):
    queryset = Trigger.objects.all().order_by("name")
    serializer_class = TriggerSerializer
    permission_classes = [IsAdminUser]


class TriggerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer
    permission_classes = [IsAdminUser]


class NotificationTemplateListCreateView(generics.ListCreateAPIView):
    queryset = NotificationTemplate.objects.select_related(
        "trigger"
    ).all().order_by("trigger__name", "channel")
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]


class NotificationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationTemplate.objects.select_related(
        "trigger"
    ).all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]


class PushSubscriptionCreateView(generics.CreateAPIView):
    serializer_class = PushSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationLogListView(generics.ListAPIView):
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return NotificationLog.objects.select_related(
            "user",
            "trigger",
            "template",
        ).all().order_by("-created_at")

class NotificationTemplateTestView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, template_id):
        try:
            template = NotificationTemplate.objects.get(
                id=template_id
            )
        except NotificationTemplate.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Template not found."
                },
                status=404
            )

        user = request.user

        notification = NotificationService.prepare_notification(
            template,
            user
        )

        if template.channel == "email":
            from .services.email_service import EmailService

            result = EmailService.send(
                to_email=user.email,
                subject=notification["subject"],
                body=notification["body"],
            )

        elif template.channel == "whatsapp":
            from .services.whatsapp_service import WhatsAppService

            phone_number = getattr(
                getattr(user, "profile", None),
                "phone_number",
                None,
            )

            if not phone_number:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Your user profile does not have "
                            "a WhatsApp phone number."
                        ),
                    },
                    status=400
                )

            result = WhatsAppService.send(
                to_phone=phone_number,
                message=notification["body"],
            )

        # elif template.channel == "web_push":
        #     return Response(
        #         {
        #             "success": False,
        #             "message": (
        #                 "Web Push test is not implemented yet."
        #             ),
        #         },
        #         status=400
        #     )
        elif template.channel == "web_push":
            from .services.onesignal_service import OneSignalService
            from .models import PushSubscription

            subscription = PushSubscription.objects.filter(
                user=user
            ).first()

            if not subscription:
                return Response(
                    {
                        "success": False,
                        "message": "No Web Push subscription found for your user.",
                    },
                    status=400,
                )

            result = OneSignalService.send(
                subscription_id=subscription.subscription_id,
                title=notification["title"],
                body=notification["body"],
            )

        else:
            return Response(
                {
                    "success": False,
                    "message": "Unsupported notification channel."
                },
                status=400
            )
        #
        # return Response(
        #     {
        #         "success": result.get("success", False),
        #         "channel": template.channel,
        #         "message": (
        #             "Test notification sent successfully."
        #             if result.get("success")
        #             else "Test notification failed."
        #         ),
        #         "response": result.get("response"),
        #     }
        # )
        print("TEST RESULT:", result)
        return Response(
            {
                "success": result.get("success", False),
                "channel": template.channel,
                "message": (
                    "Test notification sent successfully."
                    if result.get("success")
                    else "Test notification failed."
                ),
                "response": result.get("response"),
            },
            status=200 if result.get("success") else 400,
        )