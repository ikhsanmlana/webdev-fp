from flask import render_template, flash, redirect, url_for, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.users.forms import RegistrationForm, LoginForm, RolesForm
from flaskclub.models import Student, BinusID, Clubs
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

@users.route("/<int:club_id>/edit_roles", methods=['GET','POST'])
@login_required
def edit_roles(club_id):
	form = RolesForm()
	club = Clubs.query.get_or_404(club_id) 

	if (current_user.role == 'president') or (current_user.role == 'admin') : 
		if form.validate_on_submit():  
			user = Student.query.filter_by(id=form.student_id.data).first() 
			if club_id == user.club_id:

				user.role = form.roles.data

				db.session.commit()

				flash('Role has been changed.', 'success') 

				return redirect(url_for('users.edit_roles', club_id=club_id)) 
			else:
				flash('User is not in this club', 'danger') 
				return redirect(url_for('users.edit_roles', club_id=club_id)) 

	else: 
		print(form.errors)
		flash('You are not permitted', 'danger') 
		return redirect(url_for('main.home')) 

	return render_template('edit_roles.html', title="Edit Roles", form=form, club=club)
