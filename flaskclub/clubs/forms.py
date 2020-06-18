from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email 
from flaskclub.models import Clubs


class JoinForm(FlaskForm):
	submit = SubmitField('Join') 
	edit = SubmitField('Add Activity') 
	delete = SubmitField('Delete Activity')


class ActivityForm(FlaskForm):
	title = StringField('Activity Name', validators=[DataRequired(), Length(min=2)]) 
	picture = FileField('Insert Image', validators=[FileAllowed(['jpg', 'png'])])
	add = SubmitField('Add Activity') 


class NewClubForm(FlaskForm):
	id =  StringField('Club ID', validators=[DataRequired(), Length(min=1)]) 
	name = StringField('Club Name', validators=[DataRequired(), Length(min=2)]) 
	acronym = StringField('Acronym', validators=[DataRequired(), Length(min=2)]) 
	contact = StringField('Contact', validators=[DataRequired(), Length(min=2)]) 
	picture = FileField('Insert Image', validators=[FileAllowed(['jpg', 'png'])]) 
	email = StringField('Email', validators=[DataRequired(), Email()]) 
	add = SubmitField('Add Club')  

	def validate_id(self, id):
		club_id = Clubs.query.filter_by(id=id.data).first()

		if club_id: 
			raise ValidationError('Club ID is already registered.') 