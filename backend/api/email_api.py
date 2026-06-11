import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_contact_email(name: str, email: str, message: str) -> dict:
    """
    Sends an email through Gmail SMTP.
    Returns a dictionary: {status: True/False, error: "..."}
    """

    try:
        # ---------------------
        # EMAIL CONFIGURATION
        # ---------------------
        system_email = "streetbase5@gmail.com"          # Sender Gmail
        system_password = "ydht qkyo iwsh fduk"         # App password
        receiver_email = "streetbase5@gmail.com"        # Inbox where you receive messages

        # ---------------------
        # CREATE EMAIL CONTENT
        # ---------------------
        msg = MIMEMultipart()
        msg["From"] = system_email
        msg["To"] = receiver_email
        msg["Subject"] = f"StreetBase Contact Form - Message from {name}"

        body = f"""
You received a new message from the StreetBase Contact Form:

----------------------------------------
Name: {name}
Email: {email}
----------------------------------------

Message:
{message}
"""

        msg.attach(MIMEText(body, "plain"))

        # ---------------------
        # SEND EMAIL
        # ---------------------
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(system_email, system_password)
            server.send_message(msg)

        return {"status": True}

    except Exception as e:
        return {"status": False, "error": str(e)}
