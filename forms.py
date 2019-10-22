from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(FlaskForm):
    fname = StringField("First name",
                        validators=[DataRequired(), Length(min=2, max=75)])
    mname = StringField("Middle name",
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

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                        validators=[DataRequired()])
    remember = BooleanField("Remeber me")
    submit = SubmitField("Log In")