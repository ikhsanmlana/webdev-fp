from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskclub.models import Student

class RegistrationForm(FlaskForm):
	student_id = StringField('Student ID', validators=[DataRequired(), Length(min=1, max=10)])
	batch = StringField('Batch (e.g. 2021)', validators=[DataRequired(), Length(min=3, max=4)])
	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2)])
	lastname = StringField('Last Name', validators=[DataRequired()])
	gender = SelectField('Gender', choices=[('M', 'Male'), ('F','Female')])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), ])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
	submit = SubmitField('Register')

	def validate_student_id(self, student_id):
		studentid = Student.query.filter_by(id=student_id.data).first()

		if studentid: 
			raise ValidationError('Student ID is already registered with an existing account') 

	def validate_email(self, email):
		email = Student.query.filter_by(email=email.data).first()

		if email: 
			raise ValidationError('Email is already registered') 


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')