import secrets, os, datetime
from flask import render_template, flash, redirect, url_for
from flaskclub import app, db, bcrypt
from flaskclub.forms import RegistrationForm, LoginForm, JoinForm, ActivityForm, DeleteForm, PostForm, ReplyForm
from flaskclub.models import Student, Clubs, Activities, BinusID, person, Post, Reply
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
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
	return render_template('profile.html', title='Profile') 

@app.route("/clubs", methods=['GET','POST'])
def clubs(): 

	all_clubs = Clubs.query.all()
	return render_template('clubs.html', title='Clubs', clubs=all_clubs)

@app.route("/club/<int:club_id>", methods=['GET','POST'])
def club_detail(club_id):
	form = JoinForm() 
	club = Clubs.query.get_or_404(club_id) 
	all_activities = Activities.query.all()

	if form.validate_on_submit(): 
		if current_user.is_authenticated:
			flash('Club join request sent! Please wait for your approval.', 'success') 
			db.create_all()
			club.people.append(current_user)
			db.session.commit()

			return redirect(url_for('club_detail', club_id=club_id)) 
		else: 
			flash('You need to Log In first.', 'danger') 
			return redirect(url_for('club_detail', club_id=club_id)) 

	return render_template('details.html', title=club.name, club=club, activities=all_activities, form=form)

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext 
	picture_path = os.path.join(app.root_path, 'static/activity_image', picture_fn)
	form_picture.save(picture_path)

	return picture_fn

@app.route("/<int:club_id>/add_activity", methods=['GET','POST']) 
@login_required 
def add_activity(club_id):
	form = ActivityForm()
	club = Clubs.query.get_or_404(club_id) 


	if (current_user.role != 'member') or (current_user.role != ''): 
		if form.validate_on_submit(): 
			if form.picture.data: 
				picture_file = save_picture(form.picture.data)
				activity = Activities(name=form.title.data, club_id=club_id, image_file=picture_file, date_posted=datetime.date.today()) 
				
				db.session.add(activity)
				db.session.commit()

				flash('Activity Posted!', 'success') 

				return redirect(url_for('club_detail', club_id=club_id)) 
			else: 
				flash('Error', 'danger') 
				return redirect(url_for('add_activity', club_id=club_id)) 

	return render_template('add_activity.html', title=club.name, form=form, club=club)

# @app.route("/<int:club_id>/delete_activity", methods=['GET','POST']) 
# @login_required 
# def delete_activity(club_id):
# 	form = DeleteForm() 
# 	club = Clubs.query.get_or_404(club_id) 
	
# 	activity_list = Activities.query.filter_by(club_id=club_id)
# 	form.activity.choices = [(activity.id, activity.name) for activity in activity_list]

# 	if (current_user.role != 'member') or (current_user.role != ''): 
# 		if form.validate_on_submit(): 
# 			Activities.query.filter_by(id=form.activity.data).delete()

# 			db.session.commit()
# 			flash('Activity Deleted!', 'success') 

# 			return redirect(url_for('club_detail', club_id=club_id)) 
			
# 		else: 
# 			print(form.errors)
# 			flash('Error', 'danger')
# 			return redirect(url_for('club_detail', club_id=club_id)) 

# 	return render_template('delete_activity.html', title=club.name, form=form, club=club)

@app.route("/forums")
def forums():
    posts = Post.query.all()
    return render_template('forums.html', posts=posts)

@app.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id) 
    replies = Reply.query.filter_by(post_id=post_id)
    return render_template('post.html', title=post.title, post=post, replies=replies)

@app.route("/add_post", methods=['GET','POST']) 
@login_required 
def add_post():
	form = PostForm()

	if form.validate_on_submit():
	    post = Post(title=form.title.data, content=form.content.data, author=current_user)
	    db.session.add(post)
	    db.session.commit()
	    flash('Post has been created!', 'success')
	    return redirect(url_for('forums'))

	return render_template('add_post.html', title='Add Post', form=form, legend="New Post")

@app.route("/add_reply/<int:post_id>", methods=['GET','POST']) 
@login_required 
def add_reply(post_id):
	form = ReplyForm()

	if form.validate_on_submit():
	    reply = Reply(content=form.content.data, user_id=current_user.id, post_id=post_id, author=current_user)
	    db.session.add(reply)
	    db.session.commit()
	    flash('Reply has been posted!', 'success')
	    return redirect(url_for('post', post_id=post_id))

	return render_template('add_reply.html', title='Post A Reply', form=form, legend="New Reply")
