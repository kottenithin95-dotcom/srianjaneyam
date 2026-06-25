from django.db.models.signals import post_save
from threading import Thread
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from store.email_messages import (
    payment_verified_message,
    payment_failed_message,
    out_for_delivery_message,
    delivered_message,
    cod_order_messagee,
    upi_order_message,
    packed_message,
    shipped_message,
    cancelled_message,
)

from .models import Order,Payment

def send_email_async(subject, message, recipient):

    Thread(
        target=send_mail,
        args=(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient]
        ),
        kwargs={
            "fail_silently": True
        }
    ).start()


@receiver(post_save, sender=Order)
def order_status_email(sender, instance, created, **kwargs):

    if created:
        return

    user_email = instance.user.email

    # ORDER PACKED
    if instance.status == "packed":

        message = packed_message(
            instance.user,
            instance
        )

        send_email_async(
            "Order Packed",
            message,
            user_email
        )

    # ORDER SHIPPED
    elif instance.status == "shipped":

        message = shipped_message(
            instance.user,
            instance
        )

        send_email_async(
            "Order Shipped",
            message,
            user_email
        )

    # ORDER CANCELLED
    elif instance.status == "cancelled":

        message = cancelled_message(
            instance.user,
            instance
        )

        send_email_async(
            "Order Cancelled",
            message,
            user_email
        )

    # OUT FOR DELIVERY
    elif instance.status == "out_for_delivery":

        message = out_for_delivery_message(
            instance.user,
            instance
        )

        send_email_async(
            "Your Order Is Out For Delivery",
            message,
            user_email
        )

    # ORDER DELIVERED
    elif instance.status == "delivered":

        message = delivered_message(
            instance.user,
            instance
        )

        send_email_async(
            "Order Delivered Successfully",
            message,
            user_email
        )






@receiver(post_save, sender=Payment)
def payment_status_email(sender, instance, created, **kwargs):

    # NEW PAYMENT CREATED (User just placed the order)
    if created:

        if instance.method == "cod":

            # Confirm COD order
            instance.order.status = "confirmed"
            instance.order.save(update_fields=["status"])

            message = cod_order_messagee(
                instance.order.user,
                instance.order,
            )

        else:

            # UPI payment is pending
            message = upi_order_message(
                instance.order.user,
                instance.order,
                instance.transaction_id
            )

        send_email_async(
            "Order Confirmation",
            message,
            instance.order.user.email
        )

        return

    # PAYMENT SUCCESS
    if instance.status == "success":

        if instance.method != "cod":

            instance.order.status = "confirmed"
            instance.order.save(update_fields=["status"])

        message = payment_verified_message(
            instance.order.user,
            instance.order
        )

        send_email_async(
            "Payment Verified Successfully",
            message,
            instance.order.user.email
        )

    # PAYMENT FAILED
    elif instance.status == "failed":

        instance.order.status = "cancelled"
        instance.order.save(update_fields=["status"])

        message = payment_failed_message(
            instance.order.user,
            instance.order
        )

        send_email_async(
            "Payment Verification Failed",
            message,
            instance.order.user.email
        )