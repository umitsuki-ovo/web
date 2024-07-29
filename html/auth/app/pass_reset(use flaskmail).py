from flask import Blueprint, request, jsonify, url_for, render_template_string, render_template
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from app import app, db, mail, User

pass_reset_bp = Blueprint('pass_reset', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Reset app
@pass_reset_bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        token = s.dumps(email, salt='password-reset')
        reset_url = url_for('pass_reset.reset_password', token=token, _external=True)
        # Here can change message
        html = f'''
        <h1>Hi {user.username},</h1>
        <p>To reset your password, click the link below:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request a password reset, please ignore this email.</p>
        '''
        msg = Message('Password Reset Request', sender=os.environ.get('MAIL_USERNAME'), recipients=[email])
        msg.html = html
        mail.send(msg)
    json = {'message': 'Cheack your mail.', 'p': 'If your email is registered, you will receive a password reset link.'}
    return render_template('./redirect_page/correct.html', json=json)

# Reset page
@pass_reset_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=600)
    except:
        json = {'message': 'Link error', 'p': 'The password reset link is invalid or has expired.'}
        return render_template('./redirect_page/error.html', json=json)
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if password != password_confirm:
            json = {'message': 'Passwords do not match.', 'p': 'Re-enter your passwords.'}
            return render_template('./redirect_page/error.html', json=json)
        user = User.query.filter_by(email=email).first_or_404()
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        json = {'message': 'Your password has been reset.', 'p': 'You can login new passwords.'}
        return render_template('./redirect_page/correct.html', json=json)
    return render_template('./auth/reset_password_request.php')

# Mail page
@pass_reset_bp.route('/pass_reset')
def pass_reset():
    return render_template('./auth/reset_password_request.php')
