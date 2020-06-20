from flask import render_template, flash, redirect, url_for, Blueprint, abort, request
from flaskclub import app, db, bcrypt
from flaskclub.models import Activities
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	activities = Activities.query.paginate(page=page, per_page = 6)

	return render_template('home.html', activities=activities)