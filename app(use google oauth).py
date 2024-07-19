from flask import Flask, session, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import secrets
import sys
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__, static_folder='html', template_folder='html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Only for testing

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default='user')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def run():
    return render_template('index.html')

sys.path.append(os.path.join(os.path.dirname(__file__), 'html/auth/app'))

from signup import signup_bp
from login import login_bp
from pass_reset import pass_reset_bp

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(pass_reset_bp)

def send_email(to, subject, body):
    credentials = Credentials.from_authorized_user_file('****.json') #Your client json file
    service = build('gmail', 'v1', credentials=credentials)
    message = {
        'raw': base64.urlsafe_b64encode(
            f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}".encode("utf-8")
        ).decode("utf-8")
    }
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f'Message Id: {send_message["id"]}')

# if __name__ == '__main__':
#     app.run(debug=True)

