from flask import Blueprint, request, jsonify, render_template
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))


from app import app, db, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/change_role', methods=['POST'])
def change_role():
    username = request.form.get('username')
    new_role = request.form.get('role')
    
    if new_role not in ['user', 'admin']:
        return jsonify({'message': 'Invalid role. Must be "user" or "admin".'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    
    user.role = new_role
    db.session.commit()
    return jsonify({'message': f'User {username} role changed to {new_role}.'}), 200
