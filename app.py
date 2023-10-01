from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_mail import Mail
import os

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "You needs to be logged in to view this page"
login_manager.login_message_category = "error"

from App.admin import admin
from App.error import error
from App.main import main
from App.book import book
from App.auth import auth
from Api.api import api
from models import *
from App.cli import create_admin

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(book)
app.register_blueprint(admin)
app.register_blueprint(error)

api.init_app(app)

app.cli.add_command(create_admin)

@app.route('/display-image/<filename>')
def display_image(filename):
    return send_from_directory('static/images/', path=filename)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run()