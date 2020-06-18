from flask import render_template, flash, redirect, url_for, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.users.forms import RegistrationForm, LoginForm, RolesForm, UpdateAccountForm
from flaskclub.models import Student, BinusID, Clubs, Admin
from flask_login import login_user, current_user, logout_user, login_required
from flaskclub.users.utils import save_picture_profile

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
	# else:
	# 	flash('Please fill the data required for registration correctly.', 'danger')

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

@users.route("/profile/<id>", methods=['GET', 'POST'])
def profile(id):
	myclub = Clubs.query.get_or_404(current_user.club_id) 
	club = Clubs.query.all() 
	student = Student.query.get_or_404(id)
	
	return render_template('profile.html', title='Profile', myclub=myclub, student=student, club=club) 

@users.route("/<int:club_id>/edit_roles", methods=['GET','POST'])
@login_required
def edit_roles(club_id):
	form = RolesForm()
	club = Clubs.query.get_or_404(club_id) 

	


	if (current_user.role == 'president') or (current_user.role == 'admin') : 
		if form.validate_on_submit():  
			user = Student.query.filter_by(id=form.student_id.data).first() 
			for club in user.clubs:  
				if club.id == club_id: 
					user.role = form.roles.data
					user.club_id = club_id

					db.session.commit()

					flash('Role has been changed.', 'success') 

					return redirect(url_for('users.edit_roles', club_id=club_id))
			flash('User is not in this club', 'danger') 
			return redirect(url_for('users.edit_roles', club_id=club_id)) 

	else: 
		print(form.errors)
		flash('You are not permitted', 'danger') 
		return redirect(url_for('main.home')) 

	return render_template('edit_roles.html', title="Edit Roles", form=form, club=club)

@users.route("/update_profile/<id>", methods=['GET','POST']) 
@login_required 
def change_image(id):
	form = UpdateAccountForm()

	if current_user.is_authenticated:
		if form.validate_on_submit(): 
			if form.picture.data: 
				picture_file = save_picture_profile(form.picture.data)
				current_user.image_file = picture_file
				
				db.session.commit()

				flash('Image Updated!', 'success') 

				return redirect(url_for('users.profile', id=id)) 
			else: 
				flash('Error', 'danger') 
				return redirect(url_for('users.change_image', id=id)) 

	return render_template('update_profile.html', title="Profile", form=form) 

@users.route("/update_profile/delete/<id>", methods=['POST'])
@login_required
def delete_picture(id): 
	if current_user.is_authenticated: 
		if current_user.image_file != 'default.jpg':
			if current_user.id == id: 
				current_user.image_file = 'default.jpg'

				db.session.commit()
				flash('Picture removed.', 'success')
				return redirect(url_for('users.profile', id=id))
		else:
			flash('Picture removed.', 'success')
			return redirect(url_for('users.change_image', id=id)) 

@users.route("/<role>/dashboard", methods=['GET', 'POST']) 
@login_required 
def dashboard(role):
	
	return render_template('dashboard.html') 
