import os
from flask_mail import Message

class EmailService:
    def __init__(self, mail):
        self.mail = mail

    def send_reset_email(self, to_email, token):
        msg = Message(
            "Solicitud de restablecimiento de contraseña | SGSA IBCI",
            sender=os.environ.get("EMAIL_HOST_USER"),
            recipients=[to_email]
        )
        reset_link = f"http://localhost:4200/reset-password/{token}"  
        msg.html = f"""
        <html>
        <body>
            <p>Para restablecer su contraseña, haga clic en el botón siguiente:</p>
            <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; font-size: 16px; font-family: Arial, sans-serif; color: white; background-color: #007BFF; text-decoration: none; border-radius: 5px;">
                Restablecer Contraseña
            </a>
            <p>Si no realizó esta solicitud, simplemente ignore este correo electrónico y no se realizarán cambios.</p>
        </body>
        </html>
        """
        self.mail.send(msg)
