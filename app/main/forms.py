from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length

def timeout():
    dict={}
    keys = range(1,30)
    for i in keys:
        dict[i]=i
    return dict

class CallforwardForm(FlaskForm):
    exten = StringField('User', validators=[DataRequired(message='INPUT LOCAL NUMBER'),
                    Length(min=4, max=4, message='LENGTH NUMBER: 4')])
    forward_phone = StringField('Mobile', validators=[DataRequired(message='INPUT PHONE NUMBER'),
                    Length(min=11, max=11, message='LENGTH NUMBER: 11')])
    timeout = SelectField('Timeout', choices=timeout(), default=8)
    submit = SubmitField('Submit')