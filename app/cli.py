import click
from flask.cli import with_appcontext
from app.seeds import seed_all

@click.command('seed')
@with_appcontext
def seed_command():
    seed_all()
