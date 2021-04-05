from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class UserForm(FlaskForm):
    fullname = StringField('Fullname')
    username = StringField('Username')
    roles = SelectField('Role', choices={'Admin', 'Operator', 'User'}, default='User')
    submit = SubmitField('Sign In')

