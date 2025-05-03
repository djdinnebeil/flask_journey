from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "error")
            return abort(403)  # Forbidden
        return view_func(*args, **kwargs)
    return wrapper
