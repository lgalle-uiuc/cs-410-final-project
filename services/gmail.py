import smtplib
import os
from email.message import EmailMessage
import uuid 
from typing import Optional
import imaplib
import email

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
            msg["References"] = f"{references}"
        else:
            msg["References"] = reply_to

    msg.set_content(body)

    send_message(msg)

    return message_id

# https://stackoverflow.com/questions/75908727/reading-emails-with-python
def retrieve_email():
    # for simplicity, we are just retrieving all emails 

    username = os.getenv("GMAIL_EMAIL")            
    password = os.getenv("GMAIL_APP_PASSWORD")  

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')

    # Search for all email messages in the inbox
    status, data = mail.search(None, 'ALL')

    

    # Iterate through each email message and print its contents
    for num in data[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        print('From:', email_message['From'])
        print('Subject:', email_message['Subject'])
        print('Date:', email_message['Date'])
        print('Body:', email_message.get_payload())
        print('References:', email_message['References'])
        print('Reply To:', email_message['Reply-To'])
        print('Message Id', email_message['Message-Id'])
        print()
        
    # Close the connection
    mail.close()
    mail.logout()