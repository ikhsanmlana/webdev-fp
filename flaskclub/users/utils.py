import secrets, os
from flaskclub import app


def save_picture_profile(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext 
	picture_path = os.path.join(app.root_path, 'static/profile_picture', picture_fn)
	form_picture.save(picture_path)

	return picture_fn