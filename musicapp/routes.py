from musicapp import app
from flask import render_template, flash, redirect, url_for
from musicapp.forms import SignUpForm, LoginForm
from musicapp.models import User, Song, Admin, Podcast, Playlist

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