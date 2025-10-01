from flask_mail import Mail, Message
import os

mail = Mail()

def send_alert(subject, body, recipients):
    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body
        )
        mail.send(msg)
        print("=================")
        print("Email sent")
        print("=================")
        return True
    except Exception as e:
        print("=================")
        print(f"Error sending alert: {e}")
        print("=================")
        return False
