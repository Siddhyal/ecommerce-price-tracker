import os
import smtplib

from email.message import EmailMessage


def check_price_drop(current_price, target_price):
    """
    Check whether the current price has reached
    or fallen below the target price.
    """

    return current_price <= target_price


def calculate_savings(current_price, target_price):
    """
    Calculate the difference between the target
    price and current price.
    """

    return target_price - current_price


def send_price_alert(
    product_name,
    current_price,
    target_price,
    receiver_email
):
    """
    Send a price-drop notification email.
    """

    sender_email = os.getenv("PRICE_TRACKER_EMAIL")
    sender_password = os.getenv("PRICE_TRACKER_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError(
            "Email credentials are not configured."
        )

    message = EmailMessage()

    message["Subject"] = (
        f"🎉 Price Drop Alert: {product_name}"
    )

    message["From"] = sender_email
    message["To"] = receiver_email

    message.set_content(
        f"""
Price Drop Alert!

Product:
{product_name}

Current Price:
£{current_price:.2f}

Your Target Price:
£{target_price:.2f}

The product has reached your target price.

Happy shopping! 🛒
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(message)

    return True