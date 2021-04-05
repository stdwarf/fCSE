import ldap
import app
from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_login import current_user, login_required, logout_user
from datetime import datetime, timedelta
from app import db, admin_required, operator_required, user_required
from app.main.forms import CallforwardForm
from app.models import Callforward
from app.main import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        now = datetime.now()
        db.session.commit()
        try:
            last_active = session['last_active']
            flash(session['last_active'])
            delta = now - last_active
            if delta.seconds > current_app.config['SESSION_TIMER_CUSTOM']:
                session['last_active'] = now
                logout_user()
                return redirect(url_for('auth.login'))
        except:
            pass
        try:
            session['last_active'] = now
        except:
            pass
    else:
        return redirect(url_for('auth.login'))

def get_ldap_connection():
    conn = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn


@bp.route('/')
@bp.route('/index')
@login_required
@operator_required
def index():
    form = CallforwardForm()
    callforward_data = Callforward.query.order_by(Callforward.exten).all()
    return render_template("index.html", callforward_data=callforward_data, form=form)


# insert data to mysql database via html forms
@bp.route('/insert', methods=['POST'])
@login_required
@operator_required
def insert():
    form = CallforwardForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        fwd = Callforward.query.filter_by(exten=form.exten.data).first()
        if fwd:
            flash('Callforward exist')
            return redirect(url_for('main.index'))
#          if request.method == 'POST':
        exten = form.exten.data
        forward_phone = form.forward_phone.data
        timeout = form.timeout.data
        my_data = Callforward(exten, forward_phone, timeout)
        db.session.add(my_data)
        db.session.commit()
        flash("Callforward Inserted Successfully")
      else:
        flash("Wrong insert")

    return redirect(url_for('main.index'))


# update Callforward
@bp.route('/update/<id>', methods=['POST'])
@login_required
@operator_required
def update(id):
    form = CallforwardForm()
    if request.method == 'POST':
        my_data = Callforward.query.filter_by(id=id).first_or_404()
        my_data.exten = form.exten.data
        my_data.forward_phone = form.forward_phone.data
        my_data.timeout = form.timeout.data
        db.session.commit()
        flash("Callforward Updated Successfully")
        return redirect(url_for('main.index'))


# delete Callforward
@bp.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
@operator_required
def delete(id):
    my_data = Callforward.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Callforward Deleted Successfully")
    return redirect(url_for('main.index'))
