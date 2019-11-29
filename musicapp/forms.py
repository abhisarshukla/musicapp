from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from musicapp.models import User
from musicapp import images, audios
from flask_login import current_user

class SignUpForm(FlaskForm):
    fname = StringField("First name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    lname = StringField("Last name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    username = StringField("Username",
                        validators=[DataRequired(), Length(min=2, max=32)])
    password = PasswordField("Password",
                        validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                        validators=[DataRequired()])
    remember = BooleanField("Remeber me")
    submit = SubmitField("Log In")

class UpdateAccountForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    username = StringField("Username",
                        validators=[DataRequired(), Length(min=2, max=32)])
    fname = StringField("First name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    lname = StringField("Last name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    picture = FileField("Update Profile Picture",
                        validators=[FileRequired(), FileAllowed(images, 'Upload only images!')])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken please choose a different one.')

class UploadPostForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired()])
    content = TextAreaField("Content",
                        validators=[DataRequired()])
    submit = SubmitField("Post")

class UploadSongForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired()])
    description = TextAreaField("Description",
                        validators=[DataRequired()])
    name = StringField("Song Title",
                        validators=[DataRequired()])
    album = StringField("Album",
                        validators=[DataRequired()])
    genre = StringField("Genre",
                        validators=[DataRequired()])
    artist = StringField("Artist Name",
                        validators=[DataRequired()])
    song = FileField("Browse song file",
                        validators=[FileRequired(), FileAllowed(audios, 'Upload only audio files!')])
    submit = SubmitField("Upload")

class UploadPodcastForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired()])
    description = TextAreaField("Description",
                        validators=[DataRequired()])
    name = StringField("Podcast Title",
                        validators=[DataRequired()])
    category = StringField("Category",
                        validators=[DataRequired()])
    artist = StringField("Artist Name",
                        validators=[DataRequired()])
    podcast = FileField("Browse podcast file",
                        validators=[FileRequired(), FileAllowed(audios, 'Upload only audio files!')])
    submit = SubmitField("Upload")

class SongSearchForm(FlaskForm):
    name = StringField("Song Title")
    album = StringField("Album")
    genre = StringField("Genre")
    submit = SubmitField("Search")

class PodcastSearchForm(FlaskForm):
    name = StringField("Podcast Title")
    category = StringField("Category")
    submit = SubmitField("Search")