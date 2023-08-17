from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class NAME(FlaskForm):
    string_input  = StringField("string_input"  , validators=[DataRequired()])
    number_input  = IntegerField("number_input" , validators=[DataRequired()])
    passwd_input  = PasswordField("passwd_input", validators=[DataRequired()])
    submit_input  = SubmitField("submit_input")