from flask import render_template, flash, redirect, url_for, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.users.forms import RegistrationForm, LoginForm
from flaskclub.models import Student
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET','POST'])
def register():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('home'))
	form = RegistrationForm() 

	if form.validate_on_submit(): 
		user_id = BinusID.query.filter_by(id=form.student_id.data).first()
		if user_id:
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = Student(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, gender=form.gender.data, batch=form.batch.data, id=form.student_id.data)
			user_id.email=form.email.data 
			

			db.session.add(user)
			# db.session.commit()

			# user_id.user = user.id 

			db.session.commit()

			flash('Account Created!', 'success')
			return redirect(url_for('users.login')) 

	else:
		flash('Please fill the data required for registration correctly.', 'danger')

	return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()

	if form.validate_on_submit():
		user = Student.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('main.home'))
		else:
			flash('Incorrect email or password entered.', 'danger')

	return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route("/profile")
@login_required
def profile():
	return render_template('profile.html', title='Profile') 
