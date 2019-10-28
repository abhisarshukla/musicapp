from musicapp import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from musicapp.forms import SignUpForm, LoginForm
from musicapp.models import User, Song, Admin, Podcast, Playlist
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_passw = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username = form.username.data, fname = form.fname.data,
                    mname = form.mname.data, lname = form.lname.data,
                    email = form.email.data, password = hashed_passw)
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

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')