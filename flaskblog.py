from flask import Flask, render_template, flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mblkj2cjka910a'

@app.route("/") 
@app.route("/home") 
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()

	if form.validate_on_submit():
		flash(f'Account Created!')

	return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
	app.run(debug=True)

