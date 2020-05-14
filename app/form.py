from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,AnyOf

class LogInForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired('username is required!'),Length(min=2,max=15,message="username must be between 2 and 15 characters")])
    password = PasswordField("Password",validators=[InputRequired('password is required!')])
    submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired('username is required!'),Length(min=2,max=15,message="username must be between 2 and 15 characters")])
    email = StringField('Email',validators=[InputRequired('email is required!')])
    password = PasswordField("Password",validators=[InputRequired('password is required!')])
    confirmpassword = PasswordField("ConfirmPassword",validators=[InputRequired('password is required!')])
    submit = SubmitField("Signup")

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired('email is required!')])
    submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[InputRequired('password is required!')])
    confirmpassword = PasswordField("ConfirmPassword",validators=[InputRequired('password is required!')])
    submit = SubmitField("Submit")