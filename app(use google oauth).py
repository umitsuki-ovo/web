from flask import Flask, session, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import secrets
import sys
import os

# Setup
app = Flask(__name__, static_folder='html', template_folder='html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Only for testing

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default='user')

# db create
@app.before_first_request
def create_tables():
    db.create_all()

# Index page
@app.route('/')
def run():
    return render_template('index.html')

# User index page
@app.route('/<username>/index')
def user_index(username):
    if 'user_id' in session and session.get('role') == 'admin':
        return 'Welcome to admin index page!'
    elif 'user_id' in session and User.query.filter_by(username=username).first().id == session['user_id']:
        return render_template('./user/user_index.php')
    else:
        return redirect(url_for('run'))
    
# Logout page
@app.route('/logout')
def logout():
    # session_destroy
    session.pop("user_id", None)
    session.pop("role", None)
    return redirect(url_for("run"))
    

# Auth app
sys.path.append(os.path.join(os.path.dirname(__file__), 'html/auth/app'))

from signup import signup_bp
from login import login_bp
from pass_reset import pass_reset_bp
from change_bp import change_bp
from delete import delete_bp

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(pass_reset_bp)
app.register_blueprint(change_bp)
app.register_blueprint(delete_bp)

# if __name__ == '__main__':
#     app.run(debug=True)
