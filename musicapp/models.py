from datetime import datetime
from musicapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

listened = db.Table('listened',
            db.Column('user_id' ,db.Integer, db.ForeignKey('user.id')),
            db.Column('sond_id', db.Integer, db.ForeignKey('song.id'))
)

includes = db.Table('includes',
            db.Column('playlist_id', db.Integer, db.ForeignKey('user_song_playlist.id')),
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

composed = db.Table('composed',
            db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
            db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(32), nullable=False, default='default.jpeg')
    #preflang = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    searches = db.relationship('user_search_history', backref=db.backref('user'))
    playlists = db.relationship('user_song_playlist', backref=db.backref('user'))
    songs = db.relationship('Song', secondary=listened)
    posts = db.relationship('Post', backref='author', lazy=True)
    podcasts = db.relationship('Podcast', secondary=subscribed)

    def __repr__(self):
        return f"User('{self.username}', '{self.fname}', '{self.lname}', '{self.email}', '{self.image_file}')"

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    title = db.Column(db.String(75), nullable=False)
    description = db.Column(db.String, default='No description')
    category = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_location = db.Column(db.String(20), nullable=True)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    artists = db.relationship('Artist', backref=db.backref('podcast'))

    def __repr__(self):
        return f"Podcast('{self.name}', '{self.category}', '{self.release_date}''{self.rating}')"

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    title = db.Column(db.String(75), nullable=False)
    description = db.Column(db.String, default='No description')
    #duration = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    file_location = db.Column(db.String(20), nullable=False)
    album = db.Column(db.String(75), nullable=False)
    genre = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return f"Song('{self.name}', '{self.release_date}', '{self.rating}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(75), nullable=False)
    fname = db.Column(db.String(75), nullable=False)
    lname = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return f"Admin('{self.fname}', '{self.lname}')"

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=2)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcast.id'))
    compose = db.relationship('Song', secondary=composed, backref=db.backref('composer', lazy='dynamic'))

    def __repr(self):
        return f"Artist('{self.fname}', '{self.lname}', '{self.rating}')"

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=2)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=contains)

    def __repr__(self):
        return f"Playlist('{self.id}', '{self.rating}')"

class user_song_playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=includes)

class user_search_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    searchno = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))