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
def smtp_send_email(subject: str, body: str, message_id_prefix: str, reply_to: Optional[str] = None, references: Optional[str] = None):

    username = os.getenv("GMAIL_EMAIL")        

    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = username
    msg["Subject"] = subject

    # generate random message id for mock threading
    message_id = f"<{message_id_prefix}-{uuid.uuid4()}@example.com>"
    msg["Message-ID"] = message_id

    if reply_to:
        msg["In-Reply-To"] = reply_to
    
    if references:
        msg["References"] = references

    print(msg["References"])

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

    status, data = mail.search(None, 'ALL')

    email_threads = {};

    for num in data[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])

        references = email_message['References']

        thread_id_prefix = email_message['Message-Id'].strip("<>").split("-")[0]

        if references != None:
            references = references.split(' ')

        if references == None:
            email_threads[thread_id_prefix] = build_full_email_from_email_message(email_message)
        else:
            for thread in email_threads:
                if thread == thread_id_prefix:
                    email_threads[thread_id_prefix] = email_threads[thread_id_prefix] + build_full_email_from_email_message(email_message)

    print(email_threads)
        
    mail.close()
    mail.logout()


# https://stackoverflow.com/questions/64377425/how-can-i-read-the-mail-body-of-a-mail-with-python
def build_full_email_from_email_message(email_message):
    body = email_message.get_payload(decode=True).decode('utf-8').strip()
    body = body.replace('\n', ' ').replace('\r', ' ')

    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    return f"{subject} {body} "