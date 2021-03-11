from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


def timeout():
    dict={}
    keys = range(1,30)
    for i in keys:
        dict[i]=i
    return dict

class CallforwardForm(FlaskForm):
    exten = IntegerField('User', validators=[DataRequired(), NumberRange(1000, 9999)])
    forward_phone = IntegerField('Mobile', validators=[DataRequired(), NumberRange(80000000000, 89999999999)])
    timeout = SelectField('Timeout', choices=timeout(), default=8)
    submit = SubmitField('Submit')