from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

#new CLID Class
class ClidForm(FlaskForm):
    clid_num = IntegerField('Clid_num', validators=[DataRequired(), NumberRange(1000, 99999)])
    clid_name = StringField('Clid_name', validators=[DataRequired()])
    email = StringField('Email')
    fullname = StringField('Fullname')
    department = StringField('Department')
    division = StringField('Division')
    title = StringField('Title')
    submit = SubmitField('Submit')


class ExtenForm(FlaskForm):
    username = IntegerField('Exten', validators=[DataRequired(), NumberRange(1000, 99999)])
    password = StringField('Secret', validators=[DataRequired()])
    context = SelectField('Context', choices={'users', 'trunk', 'callcentre'})
    dtmf_mode = SelectField('DTMF_Mode', choices={'rfc4733', 'inband', 'info', 'auto', 'auto_info'})
    callerid = StringField('Callerid')
    call_group = IntegerField('Call_Group', validators=[NumberRange(1, 64)])
    pickup_group = IntegerField('Pickup_Group', validators=[NumberRange(1, 64)])
    submit = SubmitField('Submit')