from flask import render_template, flash, redirect, url_for, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.models import Activities
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route("/")
def home():
	return render_template('home.html')