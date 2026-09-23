# from django.contrib import admin
#
# from .models import (
#     Trigger,
#     NotificationTemplate,
#     PushSubscription,
#     NotificationLog,
# )
#
#
# @admin.register(Trigger)
# class TriggerAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "slug",
#         "is_active",
#         "created_at",
#     )
#
#     list_filter = ("is_active",)
#     search_fields = ("name", "slug")
#
#
# @admin.register(NotificationTemplate)
# class NotificationTemplateAdmin(admin.ModelAdmin):
#     list_display = (
#         "trigger",
#         "channel",
#         "is_enabled",
#         "updated_at",
#     )
#
#     list_filter = (
#         "channel",
#         "is_enabled",
#     )
#
#
# @admin.register(PushSubscription)
# class PushSubscriptionAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "subscription_id",
#         "created_at",
#     )
#
#
# @admin.register(NotificationLog)
# class NotificationLogAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "trigger",
#         "channel",
#         "status",
#         "created_at",
#     )
#
#     list_filter = (
#         "channel",
#         "status",
#     )

from django.contrib import admin

from .models import (
    Trigger,
    NotificationTemplate,
    PushSubscription,
    NotificationLog,
)


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "slug")


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "trigger",
        "channel",
        "title",
        "is_enabled",
        "updated_at",
    )
    list_filter = (
        "channel",
        "is_enabled",
    )
    search_fields = (
        "trigger__name",
        "title",
        "subject",
        "body",
    )


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscription_id",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__username",
        "subscription_id",
    )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "trigger",
        "template",
        "channel",
        "status",
        "created_at",
    )
    list_filter = (
        "channel",
        "status",
    )
    search_fields = (
        "user__username",
        "response",
    )