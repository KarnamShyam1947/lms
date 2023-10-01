import click
from flask.cli import cli, with_appcontext
from app import db, bcrypt
from models import User

@cli.command('create-admin')
@click.argument("name")
@click.argument("email")
@click.argument("password")
@with_appcontext
def create_admin(name, email, password):
    """Pass <name> <email> <password> to create an admin"""
    admin = User(name=name, email=email, 
                 password=bcrypt.generate_password_hash(password),
                 isAdmin=1, isVerified=1)
    
    db.session.add(admin)
    db.session.commit()

    click.echo(f"User {name} is created with admin privileges")