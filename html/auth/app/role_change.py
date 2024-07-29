from flask import Blueprint, request, jsonify, render_template, redirect
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))


from app import app, db, User

admin_bp = Blueprint('admin', __name__)

# Change app
@admin_bp.route('/change_role_request', methods=['POST'])
def change_role_request():
    username = request.form.get('username')
    new_role = request.form.get('role')
    
    if new_role not in ['user', 'admin']:
        json = {'message': 'Role error.', 'p': 'Invalid role. Must be "user" or "admin".'}
        return render_template('./redirect_page/error.html', json=json)

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect('./redirect_page/404.html')
    
    # Change db data
    user.role = new_role
    db.session.commit()
    
    json = {'message': 'Sucsess!', 'p': f'User {username} role changed to {new_role}.', 'redirect_url': './'}
    return render_template('./redirect_page/correct.html', json=json)

# Change page
@admin_bp.route('/change_role')
def change_role():
    return render_template('./auth/user_role_change.php')
