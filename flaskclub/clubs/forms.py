from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class JoinForm(FlaskForm):
	submit = SubmitField('Join') 
	edit = SubmitField('Add Activity') 
	delete = SubmitField('Delete Activity')


class ActivityForm(FlaskForm):
	title = StringField('Activity Name', validators=[DataRequired(), Length(min=2)]) 
	picture = FileField('Insert Image', validators=[FileAllowed(['jpg', 'png'])])
	add = SubmitField('Add Activity') 