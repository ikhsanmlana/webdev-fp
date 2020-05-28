from flask import render_template, flash, redirect, url_for
from flaskclub import app, db, bcrypt
from flaskclub.forms import RegistrationForm, LoginForm
from flaskclub.models import Student
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/") 
@app.route("/home") 
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
		user = Student(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, gender=form.gender.data, batch=22, id=form.student_id.data)
		db.session.add(user)
		db.session.commit()
		flash('Account Created!', 'success')
		return redirect(url_for('login'))
	else:
		flash('Please fill the data required for registration correctly.', 'danger')

	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	
	if form.validate_on_submit():
		user = Student.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Incorrect email or password entered.', 'danger')

	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
	return render_tempalte('profile.html', title='Profile')