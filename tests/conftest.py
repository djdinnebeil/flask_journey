import pytest
from app import create_app
from app.core import db
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(config_class='app.config.DevelopmentConfig' ,test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
    })
    app.config.update()

    with app.app_context():
        db.create_all()
        yield app  # Run the test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_users(app):
    admin = User(username='admin', password_hash=generate_password_hash('admin'), is_admin=True)
    user = User(username='dj', password_hash=generate_password_hash('password'))
    db.session.add_all([admin, user])
    db.session.commit()
