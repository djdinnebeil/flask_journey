from app.core import db
from app.models.user import User
from werkzeug.security import generate_password_hash
from sqlalchemy import select

def seed():
    users_to_seed = [
        {"username": "admin", "is_admin": True},
        {"username": "dj",     "is_admin": False},
        {"username": "daniel", "is_admin": False},
        {"username": "jose",   "is_admin": False},
    ]

    for entry in users_to_seed:
        stmt = select(User).filter_by(username=entry["username"])
        existing = db.session.execute(stmt).scalar_one_or_none()

        if not existing:
            user = User(
                username=entry["username"],
                password_hash=generate_password_hash("admin6"),
                is_admin=entry["is_admin"]
            )
            db.session.add(user)
            print(f"Seeded user '{entry['username']}'")
        else:
            print(f"User '{entry['username']}' already exists.")

    db.session.commit()
