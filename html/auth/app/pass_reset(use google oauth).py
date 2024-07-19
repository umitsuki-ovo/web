from flask import Blueprint, request, jsonify, url_for, render_template_string, render_template
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from app import app, db, mail, User
from utils import send_email

pass_reset_bp = Blueprint('pass_reset', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@pass_reset_bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        token = s.dumps(email, salt='password-reset')
        reset_url = url_for('pass_reset_request.reset_password', token=token, _external=True)
        # here can change message
        html = f'''
        <p>Hi {user.username},</p>
        <p>To reset your password, click the link below:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request a password reset, please ignore this email.</p>
        '''
       send_email(email, 'Confirm your account', html)
    return jsonify({'message': 'If your email is registered, you will receive a password reset link.'}), 200

@pass_reset_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=600)
    except:
        return jsonify({'message': 'The password reset link is invalid or has expired.'}), 400
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if password != password_confirm:
            return jsonify({'message': 'Passwords do not match.'}), 400
        user = User.query.filter_by(email=email).first_or_404()
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        return jsonify({'message': 'Your password has been reset.'}), 200
    return render_template('./auth/reset_password_request.php')

@pass_reset_bp.route('/pass_reset')
def pass_reset():
    return render_template('./auth/reset_password_request.php')
