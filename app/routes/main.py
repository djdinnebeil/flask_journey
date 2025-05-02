from flask import Blueprint, render_template, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.core import db
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')  # You can use a simple welcome page

@main_bp.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return render_template('view_user.html', user=user.to_dict(), is_admin=current_user.is_admin)
    return jsonify({'message': 'User not found'}), 404

@main_bp.route('/users', methods=['GET'])
def get_users():
    users = db.session.scalars(db.select(User)).all()
    return jsonify([user.to_dict() for user in users])
