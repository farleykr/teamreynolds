from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5aab95404e5f97c7cb4dda4255315893'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamreynolds.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from teamreynolds import routes  # noqa: F401,E402
