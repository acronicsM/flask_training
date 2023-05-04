from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserRegisterForm(FlaskForm):
    email = StringField('E-mail', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm password', [validators.DataRequired()])
    submit = SubmitField('Register')


class UserloginForm(FlaskForm):
    email = StringField('E-mail', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    submit = SubmitField('Login')
