import secrets
import os
from PIL import Image
from musicapp import app, bcrypt, db, images, audios
from flask import render_template, flash, redirect, url_for, request
from musicapp.forms import SignUpForm, LoginForm, UpdateAccountForm, PodcastSearchForm
from musicapp.forms import UploadPodcastForm, UploadPostForm, UploadSongForm, SongSearchForm
from musicapp.models import User, Song, Podcast, Playlist, Post, Artist
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    songs = Song.query.all()
    podcasts = Podcast.query.all()
    return render_template('home.html', posts=posts, songs=songs, podcasts=podcasts, audio=audios)


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_passw = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username = form.username.data, fname = form.fname.data,
                    lname = form.lname.data, email = form.email.data,
                    password = hashed_passw)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created and you can login", "success")
        return  redirect(url_for('login'))
    return render_template("signup.html", form=form, title='Register')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('home'))
        else:
            flash(f"Incorrect password or email!", "danger")
    return render_template("login.html", form=form, title='login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account',
                            image_file=image_file, form=form)

@app.route("/upload/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = UploadPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('upload_post.html', title='New Post', form=form)

@app.route("/upload/song/new", methods=['GET', 'POST'])
@login_required
def new_song():
    form = UploadSongForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            song_file = request.files['song']
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(song_file.filename)
            song_file.filename = 'm_' + random_hex + f_ext
            audio_file = audios.save(song_file)
        artist = form.artist.data
        artist = Artist.query.filter_by(name=artist).first()
        if artist:
            artist_id = artist.id
            song = Song(name=form.name.data, album=form.album.data, genre=form.genre.data, title=form.title.data, description=form.description.data, file_location=audio_file)
            db.session.add(song)
            db.session.commit()
            song.composer.append(artist)
            db.session.commit()
            flash('Your song has been added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Entered artist does not exist', 'danger')
            return redirect(url_for('new_song'))
    return render_template('upload_song.html', title='New Song', form=form)

@app.route("/upload/podcast/new", methods=['GET', 'POST'])
@login_required
def new_podcast():
    form = UploadPodcastForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            podcast_file = request.files['podcast']
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(podcast_file.filename)
            podcast_file.filename = 'p_' + random_hex + f_ext
            audio_file = audios.save(podcast_file)
        artist = form.artist.data
        artist = Artist.query.filter_by(name=artist).first()
        if artist:
            artist_id = artist.id
            podcast = Podcast(name=form.name.data, category=form.category.data, title=form.title.data, description=form.description.data, file_location=audio_file, artists=artist)
            db.session.add(podcast)
            db.session.commit()
            flash('Your podcast has been added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Entered artist does not exist', 'danger')
            return redirect(url_for('new_song'))
    return render_template('upload_podcast.html', title='New Podcast', form=form)

@app.route("/search/song", methods=['GET', 'POST'])
def search_song():
    form = SongSearchForm()
    results = []
    if form.validate_on_submit():
        name = form.name.data
        album = form.album.data
        genre = form.genre.data
        query = Song.query
        if genre:
            query = query.filter_by(genre=genre)
        if album:
            query = query.filter_by(album=album)
        if name:
            query = query.filter_by(name=name)
        results = query.all()
        print(results)
        return render_template('result.html', title='results', results=results)
    return render_template('search_song.html', title='search song', form=form)

@app.route("/search/podcast", methods=['GET', 'POST'])
def search_podcast():
    form = PodcastSearchForm()
    results = []
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        query = Song.query
        if category:
            query = query.filter_by(category=category)
        query = query.filter_by(name=name)
        results = query.all()
        return render_template('result.html', title='results', results=results)
    return render_template('search_podcast.html', title='search podcast', form=form)
