from flaskclub import app
import secrets, os


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext 
	picture_path = os.path.join(app.root_path, 'static/activity_image', picture_fn)
	form_picture.save(picture_path)

	return picture_fn

def save_picture_club(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext 
	picture_path = os.path.join(app.root_path, 'static/club_image', picture_fn)
	form_picture.save(picture_path)

	return picture_fn