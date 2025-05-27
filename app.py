from flask import Flask, render_template, redirect, url_for, session, flash
from database import init_db, create_admin_user
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.api_routes import api_bp
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    """Home page - redirect based on user type"""
    if 'user_id' in session:
        if session.get('user_type') == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure database is initialized
    init_db()
    create_admin_user()
    app.run(debug=True)
