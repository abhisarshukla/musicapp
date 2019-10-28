from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from musicapp.models import User

class SignUpForm(FlaskForm):
    fname = StringField("First name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    mname = StringField("Middle name",
                        validators=[Length(max=75)])
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

    def validate_email(self, field):
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