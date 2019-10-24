from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c730fd262264de702b0772bfb482e959'



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

folders = [
	{
		'title': 'pdf',
		'date_created' : 'October 24, 2019',
		'link' : 'home',
		'current_location': 'drive'
	},
	{
		'title': 'word',
		'date_created' : 'October 24, 2019',
		'link' : 'home',
		'current_location': 'drive'
	},
	{
		'title': 'Images',
		'date_created' : 'October 24, 2019',
		'link' : 'about',
		'current_location': 'word'
	}
]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', posts=posts, title='About')

@app.route("/drive")
def drive():
	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	return render_template('drive.html', title='Drive', image_file = folder_icon, folders= folders)

@app.route("/register")
def register():
	form = RegistrationForm()
	return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)
if __name__ == '__main__':
    app.run(debug=True)