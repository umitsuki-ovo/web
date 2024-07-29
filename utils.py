from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to, subject, body):
    # Load google oauth2 token
    credentials = Credentials.from_authorized_user_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')) # Your token file
    service = build('gmail', 'v1', credentials=credentials)
    message = MIMEMultipart('alternative')

    # Create html mail
    message['To'] = to
    message['Subject'] = subject
    mime_text = MIMEText(body, 'html')
    message.attach(mime_text)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    raw_message = {'raw': raw_message}
    send_message = service.users().messages().send(userId='me', body=raw_message).execute()

    # Debug code
    # print(f'Message Id: {send_message["id"]}')
