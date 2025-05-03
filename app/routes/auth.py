from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.core import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        next_page = request.args.get('next')
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if not user or not check_password_hash(user.password_hash, password):
            return render_template('login.html', error='Invalid username or password.')
        login_user(user)
        return redirect(url_for('main.get_user', id=user.id))
    username_prefill = request.args.get('username', '')
    return render_template('login.html', username=username_prefill)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        auto_login = 'auto_login' in request.form

        existing = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if existing:
            return render_template('register.html', error='Username already taken.')

        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful.')
        if auto_login:
            login_user(new_user)
            return redirect(url_for('main.get_user', id=new_user.id))
        else:
            return redirect(url_for('auth.login', username=username))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/login-error', methods=['GET'])
def login_error():
    return render_template('error.html', error='You must be logged-in')
