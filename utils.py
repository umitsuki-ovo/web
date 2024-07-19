from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import os

def send_email(to, subject, body):
    credentials = Credentials.from_authorized_user_file('token.json')# Your token file
    service = build('gmail', 'v1', credentials=credentials)
    message = {
        'raw': base64.urlsafe_b64encode(
            f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}".encode("utf-8")
        ).decode("utf-8")
    }
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f'Message Id: {send_message["id"]}')

