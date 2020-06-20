import secrets, os, datetime
from flask import render_template, flash, redirect, url_for, abort, request, Blueprint, jsonify
from flaskclub import app, db, bcrypt
from flaskclub.clubs.forms import JoinForm, ActivityForm, NewClubForm
from flaskclub.models import Clubs, Activities, person, Student, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskclub.clubs.utils import save_picture, save_picture_club

api = Blueprint('api', __name__) 

@api.route('/club/json/<int:id>',methods=['GET'])
def get_club(id):
    return jsonify(Clubs.query.get_or_404(id).to_dict())

@api.route('/student/json/<int:id>',methods=['GET'])
def get_user(id):
    return jsonify(Student.query.get_or_404(id).to_dict())
    
@api.route("/allstudents/json", methods=['GET'])
def get_users():
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('per_page', 10, type=int), 100)
	data = Student.to_collection_dict(Student.query, page, per_page, 'api.get_users')
	return jsonify(data)



@api.route("/allposts/json", methods=['GET'])
def get_posts():
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('per_page', 10, type=int), 100)
	data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
	return jsonify(data)



# @api.route("/student/json/", methods=['GET'])
# def create_user():
# 	data = request.get_json() 
# 	if Student.query.filter_by(id=data['id']).first():
# 		flash('Student ID is already registered.', 'danger')
# 		return redirect(url_for('users.register'))
# 	if Student.query.filter_by(email=data['email']).first():
# 		flash('Email is already registered.', 'danger')
# 		return redirect(url_for('users.register'))


# 	response = jsonify(student.to_dict()) 
# 	response.status_code = 201 
# 	response.headers['Location'] = url_for('api.get_user', id=student.id)
