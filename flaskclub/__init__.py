from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mblkj2cjka910a'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/binus_club' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b256fa592a442f:8b5d6e97@eu-cdbr-west-03.cleardb.net/heroku_1f300328b5aa173'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flaskclub import routes