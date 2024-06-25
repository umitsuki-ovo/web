from flask import Blueprint, request, jsonify, url_for, render_template_string
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app, db, mail, User

pass_reset_bp = Blueprint('pass_reset', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@pass_reset_bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if user:
        token = s.dumps(email, salt='password-reset')
        reset_url = url_for('pass_reset.reset_password', token=token, _external=True)
        #here can change message
        html = f'''
        <p>Hi {user.username},</p>
        <p>To reset your password, click the link below:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request a password reset, please ignore this email.</p>
        '''
        msg = Message('Password Reset Request', sender=os.environ.get('MAIL_USERNAME'), recipients=[email])
        msg.html = html
        mail.send(msg)
    return jsonify({'message': 'If your email is registered, you will receive a password reset link.'}), 200

@pass_reset_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=600)  # Token valid for 10 minutes
    except:
        return jsonify({'message': 'The password reset link is invalid or has expired.'}), 400
    if request.method == 'POST':
        data = request.get_json()
        password = data['password']
        password_confirm = data['password_confirm']
        if password != password_confirm:
            return jsonify({'message': 'Passwords do not match.'}), 400
        user = User.query.filter_by(email=email).first_or_404()
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        return jsonify({'message': 'Your password has been reset.'}), 200
    return render_template('../reset_password_request.php')
