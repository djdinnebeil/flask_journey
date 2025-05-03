from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.core import db
from app.utils.decorators import admin_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/ban/<int:id>', methods=['GET'])
@admin_required
def ban_user(id):
    user = db.session.get(User, id)
    if user:
        user.banned_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404