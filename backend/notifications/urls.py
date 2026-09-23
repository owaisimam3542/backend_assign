from django.urls import path

from .views import (
    TriggerListCreateView,
    TriggerDetailView,
    NotificationTemplateListCreateView,
    NotificationTemplateDetailView,
    PushSubscriptionCreateView,
    NotificationLogListView,
    NotificationTemplateTestView,
)


urlpatterns = [
    path(
        "triggers/",
        TriggerListCreateView.as_view(),
        name="trigger-list-create",
    ),
    path(
        "triggers/<int:pk>/",
        TriggerDetailView.as_view(),
        name="trigger-detail",
    ),

    path(
        "templates/",
        NotificationTemplateListCreateView.as_view(),
        name="template-list-create",
    ),
    path(
        "templates/<int:pk>/",
        NotificationTemplateDetailView.as_view(),
        name="template-detail",
    ),

    path(
        "push-subscriptions/",
        PushSubscriptionCreateView.as_view(),
        name="push-subscription-create",
    ),

    path(
        "logs/",
        NotificationLogListView.as_view(),
        name="notification-log-list",
    ),
path(
    "templates/<int:template_id>/test/",
    NotificationTemplateTestView.as_view(),
),
]