# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as StringField and BooleanField (optional)
from wtforms import StringField, PasswordField, IntegerField # BooleanField

# Import Form validators
from wtforms.validators import DataRequired, Email, EqualTo

# Define the login form (WTForms)

class LoginForm(FlaskForm):
    username    = StringField('Username', [DataRequired(message='This field is required')])

    password = PasswordField('Password', [
                DataRequired(message='Must provide a password.')])


class VerifyForm(FlaskForm):
    username    = StringField('Username', [DataRequired(message='This field is required')])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a Secret Key.')])



class RegisterForm(FlaskForm):
    email    = StringField('Email Address', [Email(),
                DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a password.')])

    descrpt  = StringField('Description', [DataRequired(message='This field is required')])

    fname = StringField('fname', [DataRequired(message='This field is required')])
    lname = StringField('lname', [DataRequired(message='This field is required')])
