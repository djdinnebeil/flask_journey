from flask import Flask, render_template
from flask_talisman import Talisman
from app.routes import register_blueprints
from app.models.user import User
from app.core import db, migrate, login_manager, limiter, csrf
from app.cli import seed_command



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, (int(user_id)))

def create_app(config_class='app.config.Config', test_config=None):
    app = Flask(__name__)
    Talisman(app)

    # Configuration
    app.config.from_object(config_class)
    app.cli.add_command(seed_command)

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    # Set login view for @login_required redirect
    login_manager.login_view = 'auth.login_error'

    # Register blueprints
    register_blueprints(app)

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    return app
