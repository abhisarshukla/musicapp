from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from forms import SignUpForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '68307df7029781e7602f3c4e2522b875'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

listened = db.Table('listened',
            db.Column('user_id' ,db.Integer, db.ForeignKey('user.id'))
            db.Column('sond_id', db.Integer, db.ForeignKey('song.id'))
)

includes = db.Table('includes',
            db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
            db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

composed = db.Table('composed',
            db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
            db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

subscribed = db.Table('subscribed',
            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'))
)

contains = db.Table('contains',
            db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
            db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
)

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
    searches = db.relationshp('user_search_history', backref=db.backref('user'))
    playlists = db.relationship('user_song_playlist', backref=db.backref('user'))
    songs = db.relationship('Song', secondary=listened)
    podcasts = db.relationship('Podcast', secondary=subscribed)

    def __repr__(self):
        return f"User('{self.username}', '{self.fname}', '{self.lname}', '{self.email}', '{self.image_file}')"

'''
TODO:
Add constraints in rating.
Add relationships to other classes.
'''
class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_location = db.Column(db.String(20), nullale=True)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    artists = db.relationship('Artist', backref=db.backref('podcast'))

    def __repr__(self):
        return f"Podcast('{self.name}', '{self.category}', '{self.release_date}''{self.rating}')"

'''
TODO:
Add relationships to other classes.
'''
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    file_location = db.Column(db.String(20), nullable=False)
    album = db.Column(db.String(75), nullable=False)
    genre = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return f"Song('{self.name}', '{self.release_date}', '{self.rating}')"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return f"Admin('{self.fname}', '{self.lname}')"

'''
TODO:
Add relationship to other tables.
'''
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    mname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    preflang = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=2)
    podcast = db.Column(db.Integer, db.ForeignKey('podcast.id'))
    compose = db.relationship('Song', secondary=composed, backref=db.backref('conposer', lazy='dynamic'))


    def __repr(self):
        return f"Artist('{self.fname}', '{self.lname}', '{self.rating}')"

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=2)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=contains)

    def __repr__(self):
        return f"Playlist('{self.id}', '{self.rating}')"

'''
TODO:
Add relationship to other tables.
'''
class user_song_playlist(db.Model):
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=includes)

'''
TODO:
Add relationship to other tables.
'''
class user_search_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    searchno = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

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