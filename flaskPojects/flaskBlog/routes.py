from flask import render_template, url_for, flash, redirect, request
from flaskBlog import app, db, bcrypt
from flaskBlog.forms import RegistrationForm, LoginForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		"author" : "Muhammad Muneeb",
		"title" : "Blog post 1",
		"content" : "First Flask Post",
		"date_posted": "August 30, 2019"
	},
	{
		"author" : "Muhammad Uzair",
		"title" : "Blog post 2",
		"content" : "Second Flask Post",
		"date_posted": "August 31, 2019"
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created! You are now able to log in", 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next') #args is a dictionary we use get method so that if the next prameter dost not exits it gives none so dont use square brackets with the key
			return redirect(next_page) if next_page else redirect(url_for('home')) # this is done so that if login page is directed from a restricted page then after login it redirects to that page instead of home page
		else:
			flash("Login Unsuccessful, Please check your email and password" , "danger")
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file)


