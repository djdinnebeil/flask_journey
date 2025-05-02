import os

# Secret key for session management and CSRF protection
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')

# SQLite example (good for local testing)
SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_journey.db'

# Disable modification tracking (optional but recommended)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Optional: Flask-Limiter default limits
RATELIMIT_DEFAULT = "60 per minute"
