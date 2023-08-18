from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email    = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit   = SubmitField("submit")
    
class RegisterForm(FlaskForm):
    name       = StringField("name", validators=[DataRequired()])
    email      = EmailField("email", validators=[DataRequired(), Email()])
    password   = PasswordField("password", validators=[DataRequired()])
    birth_date = DateField("birth date", validators=[DataRequired()])
    submit     = SubmitField("submit")