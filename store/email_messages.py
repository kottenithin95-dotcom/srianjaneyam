def cod_order_message(user, order):

    return f"""
Dear {user.username},

Thank you for shopping with Kotte's Cart.

Your order has been placed successfully.

Order ID: {order.id}
Amount: ₹{order.totalamount}

Payment Method: Cash On Delivery (COD)

Please pay the amount at your doorstep during delivery.

Thank you for choosing Kotte's Cart.

Kotte's Cart Team
"""


def upi_order_message(
    user,
    order,
    transaction_id
):

    return f"""
Dear {user.username},

Thank you for shopping with Kotte's Cart.

Your order has been received successfully.

Order ID: {order.id}
Transaction ID: {transaction_id}
Amount: ₹{order.totalamount}

Your payment is currently under verification.

Once the transaction is verified,
your order will be confirmed and processed.

If the transaction ID is invalid,
incorrect, fake, duplicate, or
unverifiable, the order may be
cancelled after verification.

Thank you for your patience.

Kotte's Cart Team
"""




def payment_verified_message(user, order):

    
        return f"""

        Dear {user.username},

        Your payment has been successfully verified.

        Order ID: {order.id}
        Amount: ₹{order.totalamount}

        We are pleased to inform you that your order has been confirmed and is now being processed.

        Thank you for shopping with Kotte's Cart.

        Kotte's Cart Team
        """

def payment_failed_message(user, order):

       
        return f"""

Dear {user.username},

We were unable to verify the payment details provided for your order.

Order ID: {order.id}

Reason:
Invalid, incorrect, duplicate, fake, or unverifiable transaction ID.

As a result, your order has been cancelled.

If you believe this is a mistake, please contact our support team with valid payment proof.

Thank you for your understanding.

Kotte's Cart Team
"""




def out_for_delivery_message(user, order):
        
        return f"""

Dear {user.username},

Good news!

Your order is now out for delivery and will reach you soon.

Order ID: {order.id}

Please keep your phone available and be ready to receive the order.

Thank you for shopping with Kotte's Cart.

Kotte's Cart Team
"""


def delivered_message(user, order):

        return f"""

Dear {user.username},

Your order has been delivered successfully.

Order ID: {order.id}

Thank you for shopping with Kotte's Cart.

We hope you enjoy your purchase and look forward to serving you again.

Kotte's Cart Team
"""
