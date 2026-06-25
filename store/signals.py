from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from store.email_messages import (
    payment_verified_message,
    payment_failed_message,
    out_for_delivery_message,
    delivered_message,
    cod_order_message,
    upi_order_message,
)

from .models import Order,Payment

@receiver(post_save, sender=Order)
def order_status_email(sender, instance, created, **kwargs):

    if created:
        return

    user_email = instance.user.email


    if instance.status == "packed":

        send_mail(
            "Order Packed",
            f"Your order #{instance.id} has been packed.",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False
        )

    elif instance.status == "shipped":

        send_mail(
            "Order Shipped",
            f"Your order #{instance.id} has been shipped.",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False
        )

    elif instance.status == "cancelled":

        send_mail(
            "Order Cancelled",
            f"Your order #{instance.id} has been cancelled.",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False
        )


@receiver(post_save, sender=Order)
def order_status_email(sender, instance, created, **kwargs):

    if created:
        return

    user_email = instance.user.email

    if instance.status == "out_for_delivery":

        message = out_for_delivery_message(
            instance.user,
            instance
        )

        send_mail(
            "Your Order Is Out For Delivery",
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False
        )

    elif instance.status == "delivered":

        message = delivered_message(
            instance.user,
            instance
        )

        send_mail(
            "Order Delivered Successfully",
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False
        )




@receiver(post_save, sender=Payment)
def payment_status_email(sender, instance, created, **kwargs):

    # NEW PAYMENT CREATED (User just placed the order)
    if created:

        if instance.payment_method == "cod":

            # Confirm COD order
            instance.order.status = "confirmed"
            instance.order.save(update_fields=["status"])

            message = cod_order_message(
                instance.order.user,
                instance.order,
                instance.transaction_id
            )

        else:

            # UPI payment is pending
            message = upi_order_message(
                instance.order.user,
                instance.order,
                instance.transaction_id
            )

        send_mail(
            "Order Confirmation",
            message,
            settings.EMAIL_HOST_USER,
            [instance.order.user.email],
            fail_silently=False
        )

        return

    # PAYMENT SUCCESS
    if instance.status == "success":

        if instance.payment_method != "cod":

            instance.order.status = "confirmed"
            instance.order.save(update_fields=["status"])

        message = payment_verified_message(
            instance.order.user,
            instance.order
        )

        send_mail(
            "Payment Verified Successfully",
            message,
            settings.EMAIL_HOST_USER,
            [instance.order.user.email],
            fail_silently=False
        )

    # PAYMENT FAILED
    elif instance.status == "failed":

        instance.order.status = "cancelled"
        instance.order.save(update_fields=["status"])

        message = payment_failed_message(
            instance.order.user,
            instance.order
        )

        send_mail(
            "Payment Verification Failed",
            message,
            settings.EMAIL_HOST_USER,
            [instance.order.user.email],
            fail_silently=False
        )