from flask import Flask
from app.routes import register_blueprints
from app.models.user import User
from app.core import db, migrate, login_manager, limiter
from seed import seed

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, (int(user_id)))

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_pyfile('../config.py')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.create_all()
        seed()

    # Set login view for @login_required redirect
    login_manager.login_view = 'auth.login'

    # Register blueprints
    register_blueprints(app)

    return app
