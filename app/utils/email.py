import os
from flask_mail import Message
from ..app import mail

def send_reset_email(to_email, token):
    msg = Message(
        "Password Reset Request",
        sender=os.environ.get("EMAIL_HOST_USER"),
        recipients=[to_email]
    )
    reset_link = f"http://localhost:4200/reset-password/{token}"  # Enlace de restablecimiento al frontend de Angular
    msg.body = f"""To reset your password, visit the following link:
{reset_link}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
