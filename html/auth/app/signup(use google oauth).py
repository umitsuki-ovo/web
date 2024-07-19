from flask import Blueprint, request, jsonify, url_for, render_template
from werkzeug.security import generate_password_hash
import re
from itsdangerous import URLSafeTimedSerializer
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from flask_app import app, db, User, send_email

signup_bp = Blueprint('signup', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
n = 0

@signup_bp.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not re.match(r'^[a-zA-Z0-9_]{3,150}$', username):
        n += 1
        return jsonify({'message': 'Invalid username. Must be 3-150 characters and contain only letters, numbers, and underscores.'}), 400
    if not re.match(r'^[A-Za-z0-9@#$%^&+=]{8,}$', password):
        n += 1
        return jsonify({'message': 'Password must be at least 8 characters long and contain letters, numbers, and special characters.'}), 400
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        n += 1
        return jsonify({'message': 'Invalid email address.'}), 400
    if User.query.filter_by(username=username).first() is not None:
        n += 1
        return jsonify({'message': 'Username already exists.'}), 400
    if User.query.filter_by(email=email).first() is not None:
        n += 1
        return jsonify({'message': 'Email already registered.'}), 400
    if n == 0:
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash, role='user')
        db.session.add(new_user)
        db.session.commit()
        token = s.dumps(email, salt='email-confirm')
        confirm_url = url_for('signup.confirm_email', token=token, _external=True)
        #here can change message
        html = f'''
        <p>Hi {username},</p>
        <p>Thank you for signing up. Please click the link below to confirm your email address and complete your registration:</p>
        <p><a href="{confirm_url}">Confirm your email address</a></p>
        <p>If you did not sign up for this account, please ignore this email.</p>
        '''
        send_email(email, 'Confirm your account', html)
        return jsonify({'message': 'A confirmation email has been sent.'}), 201

@signup_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({'message': 'Account already confirmed. Please login.'}), 200
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'You have confirmed your account. Thanks!'}), 200

@signup_bp.route('/signup_page')
def signup_page():
    return render_template('./auth/signup.php')
