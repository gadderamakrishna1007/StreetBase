import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_quote_email(name: str, email: str, service_choice: str, message: str) -> dict:
    """
    Sends a Quote Request email via Gmail SMTP.
    
    Args:
        name (str): Client's full name.
        email (str): Client's email address.
        service_choice (str): The service they selected.
        message (str): Additional requirements.
        
    Returns:
        dict: {"status": True} if successful, {"status": False, "error": "Error message"} if failed.
    """
    try:
        # ---------------------
        # 1. CONFIGURATION
        # ---------------------
        system_email = "streetbase5@gmail.com"          
        system_password = "ydht qkyo iwsh fduk"      
        receiver_email = "streetbase5@gmail.com"        

        # ---------------------
        # 2. CREATE EMAIL
        # ---------------------
        msg = MIMEMultipart()
        msg["From"] = system_email
        msg["To"] = receiver_email
        msg["Subject"] = f"📢 New Quote Request: {service_choice} - {name}"

        body = f"""
        You have received a new Service Quote Request via StreetBase.

        ----------------------------------------
        👤 Client Name: {name}
        📧 Client Email: {email}
        🛠️ Service Interested: {service_choice}
        ----------------------------------------

        📝 Additional Requirements:
        {message if message else "No specific details provided."}
        """
        msg.attach(MIMEText(body, "plain"))

        # ---------------------
        # 3. SEND EMAIL
        # ---------------------
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(system_email, system_password)
            server.send_message(msg)

        return {"status": True}

    except Exception as e:
        # Return the error message so the frontend can display it
        return {"status": False, "error": str(e)}
