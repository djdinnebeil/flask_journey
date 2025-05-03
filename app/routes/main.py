from flask import Blueprint, render_template, jsonify, request, flash
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
        return render_template('view_user.html', user=user.to_dict())
    return render_template('error.html', message='User not found'), 404

@main_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    # users = db.session.scalars(db.select(User).where(User.deleted_at.is_(None))).all()
    users = db.session.scalars(db.select(User)).all()
    return render_template('user_list.html', users=users)

@main_bp.route('/user/<int:id>', methods=['POST'])
@login_required
def update_user(id):
    if current_user.id != id:
        flash('Unauthorized')
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form['username'].strip()
    user = db.session.get(User, id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    existing = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar_one_or_none()

    if existing and existing.id != id:
        return render_template('view_user.html', user=user.to_dict(), error='Username already taken')

    user.username = username
    db.session.commit()
    return render_template('view_user.html', user=user.to_dict(), message='User updated successfully')
