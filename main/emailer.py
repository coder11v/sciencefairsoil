import os
import smtplib
import socket
import traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

def send_error_email(error="Unknown Error", recipient_email=None):
    """
    Send an error report email to multiple recipients.
    - error: Exception or string
    - recipient_email: The primary hardcoded recipient (defaults to sender if None)
    """

    try:
        # 1. Setup Credentials
        sender_email = "financevibro@gmail.com"
        # Using pathlib to read password safely
        sender_password = Path("secrets/pw.txt").read_text().strip()
        
        # 2. Determine Recipients
        # Recipient A: The one passed as argument (or default to sender)
        primary_email = recipient_email or sender_email
        
        # Recipient B: The one from secrets/phone.txt
        phone_email = None
        try:
            phone_email_path = Path("secrets/phone.txt")
            if phone_email_path.exists():
                phone_email = phone_email_path.read_text().strip()
        except Exception:
            print("Could not read secrets/phone.txt, skipping secondary email.")

        # Build the list of valid recipients
        recipients = [primary_email]
        if phone_email:
            recipients.append(phone_email)

        if not sender_email or not sender_password:
            return False, "Email credentials not configured"

        # 3. Build message
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        # Join recipients with a comma for the header
        msg["To"] = ", ".join(recipients) 
        msg["Subject"] = "🚨 Soil Error Alert"

        timestamp = datetime.utcnow().isoformat()
        hostname = socket.gethostname()
        trace = traceback.format_exc() if isinstance(error, Exception) else "N/A"

        # Plain-text fallback
        text_content = f"""
Soil Error Alert

Time (UTC): {timestamp}
Host: {hostname}

Error:
{str(error)}

"""


        msg.attach(MIMEText(text_content, "plain"))

        # 4. Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            # send_message automatically parses the "To" header to send to all recipients
            server.send_message(msg)

        return True, f"Error email sent to {len(recipients)} recipients"

    except Exception as notify_error:
        # Never crash the app because alerting failed
        print("Failed to send error email:", notify_error)
        return False, str(notify_error)




def send_water_event_msg(pump="Unknown", recipient_email=None):
    """
    Send a watering event notification email.
    - pump: Identifier or name of the pump that activated
    - recipient_email: Primary recipient (defaults to sender if None)
    """

    try:
        # 1. Setup Credentials
        sender_email = "financevibro@gmail.com"
        sender_password = Path("secrets/pw.txt").read_text().strip()

        # 2. Determine Recipients
        primary_email = recipient_email or sender_email

        phone_email = None
        try:
            phone_email_path = Path("secrets/phone.txt")
            if phone_email_path.exists():
                phone_email = phone_email_path.read_text().strip()
        except Exception:
            print("Could not read secrets/phone.txt, skipping secondary email.")

        recipients = [primary_email]
        if phone_email:
            recipients.append(phone_email)

        if not sender_email or not sender_password:
            return False, "Email credentials not configured"

        # 3. Build message
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = "💧 Soil Watering Event"

        timestamp = datetime.utcnow().isoformat()
        hostname = socket.gethostname()

        text_content = f"""
Soil Watering Event

Time (UTC): {timestamp}
Host: {hostname}

Pump Activated:
{pump}
"""

        msg.attach(MIMEText(text_content, "plain"))

        # 4. Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True, f"Water event email sent to {len(recipients)} recipients"

    except Exception as notify_error:
        # Never crash the app because alerting failed
        print("Failed to send water event email:", notify_error)
        return False, str(notify_error)
