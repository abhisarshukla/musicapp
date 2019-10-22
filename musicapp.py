from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from forms import SignUpForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '68307df7029781e7602f3c4e2522b875'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

'''
TODO:
Add relationships to other classes.
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    preflang = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.fname}', '{self.lname}',
                '{self.email}', '{self.image_file}')"

'''
TODO:
Add constraints in rating.
Add relationships to other classes.
'''
class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

'''
TODO:
Add relationships to other classes.
'''
class songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songname = db.Column(db.String(75), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    album = db.Column(db.String(75), nullable=False)
    genre = db.Column(db.String(75), nullable=False)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)

'''
TODO:
Add relationship to other tables.
'''
class artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    preflang = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=2)

class playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=2)

'''
TODO:
Add relationship to other tables.
'''
class contains(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class composed(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class includes(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class listened(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class subscribed(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class user_song_playlist(db.Model):
    pass

'''
TODO:
Add relationship to other tables.
'''
class user_search_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    searchno = db.Column(db.Integer, nullable=False)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f"Signup successfull!", "success")
        return  redirect(url_for('home'))
    return render_template("signup.html", form=form, title='Register')

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login successfull", "success")
        return redirect(url_for('home'))
    else:
        flash(f"Incorrect password or email!", "danger")
    return render_template("login.html", form=form, title='login')