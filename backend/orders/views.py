from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Trigger
from notifications.services.notification_service import NotificationService

from .models import Order


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_number = request.data.get("order_number")
        amount = request.data.get("amount")

        if not order_number or amount is None:
            return Response(
                {
                    "success": False,
                    "message": "order_number and amount are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                amount=amount,
            )
        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            trigger = Trigger.objects.get(
                slug="order-placed",
                is_active=True,
            )
            NotificationService.dispatch(
                trigger,
                request.user,
            )
        except Trigger.DoesNotExist:
            pass
        except Exception:
            # Notification failure should not prevent order creation.
            pass

        return Response(
            {
                "success": True,
                "message": "Order placed successfully.",
                "order": {
                    "id": order.id,
                    "order_number": order.order_number,
                    "amount": str(order.amount),
                    "created_at": order.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )