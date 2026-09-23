from rest_framework import serializers

from .models import (
    Trigger,
    NotificationTemplate,
    PushSubscription,
    NotificationLog,
)


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    trigger_name = serializers.CharField(
        source="trigger.name",
        read_only=True,
    )

    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "trigger",
            "trigger_name",
            "channel",
            "title",
            "subject",
            "body",
            "is_enabled",
            "created_at",
            "updated_at",
        ]


class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = [
            "id",
            "user",
            "subscription_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = [
            "id",
            "user",
            "trigger",
            "template",
            "channel",
            "status",
            "response",
            "created_at",
        ]