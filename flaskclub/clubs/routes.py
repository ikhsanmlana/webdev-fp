import secrets, os, datetime
from flask import render_template, flash, redirect, url_for, abort, request, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.clubs.forms import JoinForm, ActivityForm
from flaskclub.models import Clubs, Activities, person
from flask_login import login_user, current_user, logout_user, login_required
from flaskclub.clubs.utils import save_picture


clubs = Blueprint('clubs', __name__)

@clubs.route("/clubs", methods=['GET','POST'])
def all_clubs(): 

	all_clubs = Clubs.query.all()
	return render_template('clubs.html', title='Clubs', clubs=all_clubs)

@clubs.route("/club/<int:club_id>", methods=['GET','POST'])
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

			return redirect(url_for('clubs.club_detail', club_id=club_id)) 
		else: 
			flash('You need to Log In first.', 'danger') 
			return redirect(url_for('clubs.club_detail', club_id=club_id)) 

	return render_template('details.html', title=club.name, club=club, activities=all_activities, form=form)


@clubs.route("/<int:club_id>/add_activity", methods=['GET','POST']) 
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

				return redirect(url_for('clubs.club_detail', club_id=club_id)) 
			else: 
				flash('Error', 'danger') 
				return redirect(url_for('clubs.add_activity', club_id=club_id)) 

	return render_template('add_activity.html', title=club.name, form=form, club=club)
