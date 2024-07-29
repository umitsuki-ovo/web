from flask import Blueprint, request, jsonify, url_for, render_template
from werkzeug.security import generate_password_hash
import re
from itsdangerous import URLSafeTimedSerializer
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from app import app, db, User
from utils import send_email

signup_bp = Blueprint('signup_request', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Signup app
@signup_bp.route('/signup_request', methods=['POST'])
def signup_request():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not re.match(r'^[a-zA-Z0-9_]{3,150}$', username):
        json = {'message': 'Invalid username.', 'p': 'Invalid username. Must be 3-150 characters and contain only letters, numbers, and underscores.'}
        return render_template('./redirect_page/error.html', json=json)
    if not re.match(r'^[A-Za-z0-9@#$%^&+=]{8,}$', password):
        json = {'message': 'Re-enter the password.', 'p': 'Password must be at least 8 characters long and contain letters, numbers, and special characters.'}
        return render_template('./redirect_page/error.html', json=json)
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        json = {'message': 'Invalid email address.', 'p': 'Please enter a valid email address.'}
        return render_template('./redirect_page/error.html', json=json)
    if User.query.filter_by(username=username).first() is not None:
        json = {'message': 'Username already exists.', 'p': 'Please enter another username.'}
        return render_template('./redirect_page/error.html', json=json)
    if User.query.filter_by(email=email).first() is not None:
        json = {'message': 'Email already registered.', 'p': 'Email already registered. You can login your account.'}
        return render_template('./redirect_page/error.html', json=json)
    
    # Add date to db
    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash, role='user')
    db.session.add(new_user)
    db.session.commit()

    # Create confirm mail
    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('signup_request.confirm_email', token=token, _external=True)
    # Here can change message
    html = f'''
    <p>Hi {username},</p>
    <p>Thank you for signing up. Please click the link below to confirm your email address and complete your registration:</p>
    <p><a href="{confirm_url}">Confirm your email address</a></p>
    <p>If you did not sign up for this account, please ignore this email.</p>
    '''
    send_email(email, 'Confirm your account', html)
    return jsonify({'message': 'A confirmation email has been sent.'}), 201

# Confirm app
@signup_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        json = {'message': 'Confirmation link error.', 'p': 'The confirmation link is invalid or has expired. Please signup one more time.'}
        return render_template('./redirect_page/error.html', json=json)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        json = {'message': 'You are already confirmed.', 'p': 'Account already confirmed. Please login.'}
        return render_template('./redirect_page/error.html', json=json)
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        json = {'message': 'Confirmation successful.', 'p': 'You have confirmed your account. Thanks!', 'redirect_url': 'https://****.com/login'}
        return render_template('./redirect_page/correct.html', json=json)

# Signup page
@signup_bp.route('/signup')
def signup():
    return render_template('./auth/signup.php')
