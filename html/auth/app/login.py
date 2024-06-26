from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))


from app import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        if user.confirmed:
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return jsonify({'message': 'Login successful.', 'redirect_url': '../../admin/admin_index.php'}), 200
            else:
                return jsonify({'message': 'Login successful.', 'redirect_url': '../../user/user_index.php'}), 200
        else:
            return jsonify({'message': 'Please confirm your email address.'}), 401
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401
    
@login_bp.route('/login_page')
def login_page():
    return render_template('./auth/login.php')
