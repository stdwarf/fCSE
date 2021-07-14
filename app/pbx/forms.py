from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, ValidationError, InputRequired


def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length

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


class AlarmForm(FlaskForm):
    play_file = SelectField('Choice', choices=[('1.1_Welcome','Уважаемые коллеги'),('2.1_Tech','В настоящее время наблюдаются технические проблемы в работе сервисов..'),
                                               ('2.2_Plan','В настоящее время проводятся плановые технические работы, затрагивающие сервисы..'),
                                               ('3.1_Email','Электронной почты'),('3.2_Kargo','Карго'),
                                               ('3.3_Net_files','Доступа к сетевым файлам'),('3.4_Pbx','Телефонии'),
                                               ('3.5_Terminal','Терминальных станций'),('3.6_Internet','Доступа в интернет'),
                                               ('3.7_Service_Desc','Сервис-деск'),('3.8_Remote_desktop','Удалённого доступа'),
                                               ('3.9_Printers','Доступа к принтерам'),('3.10_PC','Авторизации на рабочих компьютерах'),
                                               ('3.11_Mob_app','Мобильного приложения'),('3.12_Personal_area','Личного кабинета'),
                                               ('3.13_Integration','Интеграции с клиентами'),('3.14_Money','Приёма платежей'),
                                               ('4.1_Tech','Наши специалисты уже занимаются устранением сбоя. Работа сервисов будет восстановлена в максимально короткие сроки.'),
                                               ('4.2_Plan','По завершению работ, сервисы будут восстановлены.'),
                                               ('4.3_Sheet', 'С расписанием плановых работ вы можете ознакомиться на корпоративном портале.'),
                                               ('5.1_Bye','Спасибо за понимание.'),
                                               ('6.1_Portal','Вы можете самостоятельно завести заявку на портале самообслуживания, выбрав нужную категорию в каталоге услуг.')],
                            default=('1.1_Welcome','Уважаемые коллеги'))
    order = IntegerField('Order')
    #active = BooleanField('Active',default=True,render_kw ={'checked':''})
    active = BooleanField('Active')
    submit = SubmitField('Submit')


class BlacklistForm(FlaskForm):
    clid = StringField('Callerid', validators=[InputRequired(), length(min=9, max=20)])
    ticket = StringField('Ticket', validators=[InputRequired()])
    active = BooleanField('Active')
    submit = SubmitField('Submit')