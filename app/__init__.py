from flask import Flask
from app.routes import register_blueprints
from app.models.user import User
from app.core import db, migrate, login_manager, limiter, csrf
from seed import seed

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, (int(user_id)))

def create_app(config_class='app.config.Config', test_config=None):
    app = Flask(__name__)

    # Configuration
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()
        if not test_config:
            seed()

    # Set login view for @login_required redirect
    login_manager.login_view = 'auth.login_error'

    # Register blueprints
    register_blueprints(app)

    return app
