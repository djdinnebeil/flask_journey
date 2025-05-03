from functools import wraps
from flask import redirect, url_for, flash, abort, render_template
from flask_login import current_user

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            return render_template('error.html', error='You do not have permission to access this page.')
        return view_func(*args, **kwargs)
    return wrapper
