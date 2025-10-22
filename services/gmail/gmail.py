import smtplib
import os
from email.message import EmailMessage
import uuid 
from typing import Optional

# https://mailtrap.io/blog/python-send-email-gmail/
def send_message(msg):

    username = os.getenv("GMAIL_EMAIL")            
    password = os.getenv("GMAIL_APP_PASSWORD")  
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(username, password)
        s.send_message(msg)

# https://docs.python.org/3/library/email.message.html
# https://stackoverflow.com/questions/5938890/setting-different-reply-to-message-in-python-email-smtplib
def smtp_send_email(subject: str, body: str, reply_to: Optional[str] = None, references: Optional[str] = None):

    username = os.getenv("GMAIL_EMAIL")        

    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = username
    msg["Subject"] = subject

    # generate random message id for mock threading
    message_id = f"<{uuid.uuid4()}@example.com>"
    msg["Message-ID"] = message_id

    if reply_to:
        msg["Reply-To"] = reply_to
        if references:
            msg["References"] = f"{references} {reply_to}"
        else:
            msg["References"] = reply_to

    msg.set_content(body)

    send_message(msg)

    return message_id