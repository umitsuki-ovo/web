from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))


from app import User

login_bp = Blueprint('login_request', __name__)

@login_bp.route('/login_request', methods=['POST'])
def login_request():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        if user.confirmed:
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return jsonify({'message': 'Login successful.', 'p': 'Redirect user page. Wait a minute.', 'redirect_url': '../../admin/admin_index.php'}), 200
            else:
                return jsonify({'message': 'Login successful.', 'p': 'Redirect user page. Wait a minute.', 'redirect_url': '../../user/user_index.php'}), 200
        else:
            return jsonify({'message': 'Please confirm your email address.', 'p': 'Please go back to the page and re-enter your email address.'}), 401
    else:
        return jsonify({'message': 'Invalid username or password.', 'p': 'Please go back to the page and re-enter your username or password.'}), 401
    
@login_bp.route('/login')
def login():
    return render_template('./auth/login.php')
