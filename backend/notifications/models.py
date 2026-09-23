# from django.db import models
#
#
# class Trigger(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
#     is_active = models.BooleanField(default=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#
# class NotificationTemplate(models.Model):
#
#     WHATSAPP = "whatsapp"
#     EMAIL = "email"
#     WEB_PUSH = "web_push"
#
#     CHANNEL_CHOICES = [
#         (WHATSAPP, "WhatsApp"),
#         (EMAIL, "Email"),
#         (WEB_PUSH, "Web Push"),
#     ]
#
#     trigger = models.ForeignKey(
#         Trigger,
#         on_delete=models.CASCADE,
#         related_name="templates"
#     )
#
#     channel = models.CharField(
#         max_length=20,
#         choices=CHANNEL_CHOICES
#     )
#
#     title = models.CharField(
#         max_length=255,
#         blank=True
#     )
#
#     subject = models.CharField(
#         max_length=255,
#         blank=True
#     )
#
#     body = models.TextField()
#
#     is_enabled = models.BooleanField(default=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ("trigger", "channel")
#
#     def __str__(self):
#         return f"{self.trigger.name} - {self.channel}"
#
#
# class PushSubscription(models.Model):
#     user = models.ForeignKey(
#         "auth.User",
#         on_delete=models.CASCADE,
#         related_name="push_subscriptions"
#     )
#
#     subscription_id = models.CharField(
#         max_length=255,
#         unique=True
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.subscription_id}"
#
#
# class NotificationLog(models.Model):
#
#     SUCCESS = "success"
#     FAILED = "failed"
#
#     STATUS_CHOICES = [
#         (SUCCESS, "Success"),
#         (FAILED, "Failed"),
#     ]
#
#     user = models.ForeignKey(
#         "auth.User",
#         on_delete=models.CASCADE
#     )
#
#     trigger = models.ForeignKey(
#         Trigger,
#         on_delete=models.SET_NULL,
#         null=True
#     )
#
#     template = models.ForeignKey(
#         NotificationTemplate,
#         on_delete=models.SET_NULL,
#         null=True
#     )
#
#     channel = models.CharField(max_length=20)
#
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES
#     )
#
#     response = models.TextField(blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user} - {self.channel} - {self.status}"


from django.contrib.auth.models import User
from django.db import models
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class Trigger(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    CHANNEL_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("web_push", "Web Push"),
    ]

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.CASCADE,
        related_name="templates",
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
    )

    title = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()

    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trigger", "channel"],
                name="unique_trigger_channel",
            )
        ]

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"


class PushSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="push_subscriptions",
    )

    subscription_id = models.CharField(
        max_length=255,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_id}"


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notification_logs",
    )

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    channel = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    response = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel} - {self.status}"