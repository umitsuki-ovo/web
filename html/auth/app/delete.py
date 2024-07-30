from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from app import app, db, User

delete_bp = Blueprint('delete_user_request', __name__)

# Delete app
@delete_bp.route('/delete_user_request', methods=['POST'])
def delete_user_request():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        json = {'p': 'Delete successful.', 'message': "User {username} has been deleted.", 'redirect_url': './'}
        return render_template('./redirect_page/correct.html', json=json)
    else:
        json = {'message': 'Invalid username or password.', 'p': 'Please go back to the page and re-enter your username or password.'}
        return render_template('./redirect_page/error.html', json=json)
    
# Delete page
@delete_bp.route('/delete_user', methods=['POST'])
def delete_user():
    return render_template('index.html')
