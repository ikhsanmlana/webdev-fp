from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 



app = Flask(__name__)	

app.config['SECRET_KEY'] = 'very-secret-much'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/binus_club' 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b256fa592a442f:8b5d6e97@eu-cdbr-west-03.cleardb.net/heroku_1f300328b5aa173' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:binus2020@binusclubs.ch5ozsog8ncz.us-east-2.rds.amazonaws.com/binusianclubs' 
app.config['SQLALCHEMY_POOL_RECYCLE'] = 28799 

# app.config['SQLALCHEMY_BINDS'] = {'db_clubs': 'mysql://b803fbe660c487:a2a1aea1@eu-cdbr-west-03.cleardb.net/	'}

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from flaskclub.users.routes import users
from flaskclub.forum.routes import forum
from flaskclub.clubs.routes import clubs
from flaskclub.main.routes import main
from flaskclub.api.routes import api

app.register_blueprint(users)
app.register_blueprint(forum)
app.register_blueprint(clubs)
app.register_blueprint(main)
app.register_blueprint(api)