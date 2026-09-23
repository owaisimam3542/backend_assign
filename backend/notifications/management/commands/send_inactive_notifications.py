from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from notifications.models import NotificationLog, Trigger
from notifications.services.notification_service import NotificationService


class Command(BaseCommand):
    help = "Send inactive-for-1-day notifications to inactive users."

    def handle(self, *args, **options):
        try:
            trigger = Trigger.objects.get(
                slug="inactive-1-day",
                is_active=True,
            )
        except Trigger.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "Inactive for 1 Day trigger not found or inactive."
                )
            )
            return

        cutoff = timezone.now() - timedelta(days=1)

        users = User.objects.filter(
            is_active=True,
            last_login__isnull=False,
            last_login__lte=cutoff,
        )

        sent_count = 0
        skipped_count = 0

        for user in users:
            already_sent = NotificationLog.objects.filter(
                user=user,
                trigger=trigger,
                created_at__gte=cutoff,
            ).exists()

            if already_sent:
                skipped_count += 1
                continue

            NotificationService.dispatch(trigger, user)
            sent_count += 1

            self.stdout.write(
                f"Processed inactive user: {user.username}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Processed: {sent_count}, Skipped: {skipped_count}"
            )
        )