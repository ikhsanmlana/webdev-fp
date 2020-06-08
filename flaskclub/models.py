from datetime import datetime
from flaskclub import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Student.query.get(user_id)

class Student(db.Model, UserMixin): 
	__tablename__ = 'student'
	id = db.Column('student_id', db.String(10), primary_key=True) 
	firstname = db.Column('first_name', db.String(255), nullable=False) 
	lastname = db.Column('last_name', db.String(255), nullable=True) 
	email = db.Column('email', db.String(255), unique=True, nullable=False) 
	password = db.Column('password', db.String(255), nullable=False)  
	gender = db.Column('gender', db.String(255), nullable=False)  
	batch = db.Column('batch', db.Integer, nullable=False) 
	role = db.Column('role', db.String(255), nullable=True) 

	def __repr__(self):
		return f"Student('{self.firstname}', '{self.lastname}', '{self.email}')"

class Clubs(db.Model, UserMixin): 
	__tablename__ = 'clubs'
	id = db.Column('id', db.Integer, primary_key=True) 
	name = db.Column('name', db.String(255), nullable=False) 
	contact = db.Column('contact', db.String(255), nullable=True) 
	email = db.Column('email', db.String(255), nullable=True) 
	members = db.Column('members', db.Integer, nullable=False)  
	image_file = db.Column('image', db.String(20), nullable=False, default='default.jpg')	
	

	def __repr__(self):
		return f"Clubs('{self.name}')"