import json
from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, session, current_app, jsonify
from flask_login import current_user, login_required, logout_user
from app import db, admin_required, operator_required
from app.models import Clid, Ps_auths, Ps_aors, Ps_endpoints, Alarms
from app.pbx import bp
from app.pbx.forms import ClidForm, ExtenForm, AlarmForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        now = datetime.now()
        db.session.commit()
        try:
            last_active = session['last_active']
#            flash(session['last_active'])
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


@bp.route('/index')
@login_required
@admin_required
def index():
    form = ClidForm()
    clid_data = Clid.query.order_by(Clid.clid_num).all()
    return render_template("pbx/clid.html", clid_data=clid_data, form=form)


@bp.route('/update/<id>', methods=['POST'])
@login_required
@admin_required
def update(id):
    form = ClidForm()
    if request.method == 'POST':
        my_data = Clid.query.filter_by(id=id).first_or_404()
        my_data.fullname = form.fullname.data
        my_data.clid_name = form.clid_name.data
        my_data.clid_num = form.clid_num.data
        my_data.email = form.email.data
        my_data.department = form.department.data
        my_data.division = form.division.data
        my_data.title = form.title.data
        my_data.address = form.address.data
        db.session.commit()
        return jsonify(status='ok')
        flash("CLID Updated Successfully")
        return redirect(url_for('pbx.index'))


# delete employee
@bp.route('/delete/<id>/', methods=['GET', 'POST'])
@admin_required
def delete(id):
    my_data = Clid.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Clid Deleted Successfully")
    return redirect(url_for('pbx.index'))


#exten
@bp.route('/exten/index')
@login_required
@admin_required
def exten_index():
    form = ExtenForm()
    exten = Ps_auths.query.order_by(Ps_auths.id).all()
    return render_template("pbx/exten.html", exten_data=exten, form=form)


# insert data to mysql database via html forms
@bp.route('/exten/insert', methods=['POST'])
@login_required
@operator_required
def exten_insert():
    form = ExtenForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        exten = Ps_endpoints.query.filter_by(id=form.username.data).first()
        if exten:
            flash('Exten exist')
            return redirect(url_for('pbx.exten_index'))
        username = form.username.data
        password = form.password.data
        context = form.context.data
        dtmf_mode = form.dtmf_mode.data
        callerid = form.callerid.data
        call_group = form.call_group.data
        pickup_group = form.pickup_group.data
        endp = Ps_endpoints(context=context, id=username, dtmf_mode=dtmf_mode, callerid=callerid,
                            call_group=call_group, pickup_group=pickup_group, auth=username, aor=username)
        aor = Ps_aors(id=username, max_contacts=1)
        auth = Ps_auths(id=username, username=username, password=password)
        db.session.add(aor)
        db.session.add(auth)
        db.session.add(endp)
        db.session.commit()
        return jsonify(status='ok')
        flash("Exten Inserted Successfully")
      else:
        flash("Wrong insert")

    return redirect(url_for('pbx.exten_index'))


@bp.route('/exten/update/<id>', methods=['POST'])
@login_required
@admin_required
def exten_update(id):
    form = ExtenForm()
    if request.method == 'POST':
        endp = Ps_endpoints.query.filter_by(id=id).first_or_404()
        auth = Ps_auths.query.filter_by(id=id).first_or_404()
        auth.username = form.username.data
        auth.password = form.password.data
        endp.context = form.context.data
        endp.dtmf_mode = form.dtmf_mode.data
        endp.callerid = form.callerid.data
        endp.call_group = form.call_group.data
        endp.pickup_group = form.pickup_group.data
        db.session.commit()
        flash("Exten Updated Successfully")
        return redirect(url_for('pbx.exten_index'))


# delete employee
@bp.route('/exten/delete/<id>/', methods=['GET', 'POST'])
@admin_required
def exten_delete(id):
    endp = Ps_endpoints.query.get(id)
    aor = Ps_aors.query.get(id)
    auth = Ps_auths.query.get(id)
    db.session.delete(endp)
    db.session.delete(aor)
    db.session.delete(auth)
    db.session.commit()
    flash("Clid Deleted Successfully")
    return redirect(url_for('pbx.exten_index'))


@bp.route('/alarm/index')
@login_required
@operator_required
def alarm_index():
    form = AlarmForm()
    alarm_data = Alarms.query.order_by(Alarms.order).all()
    return render_template("pbx/alarm.html", alarm_data=alarm_data, form=form)


@bp.route('/alarm/insert', methods=['POST'])
@login_required
@admin_required
def alarm_insert():
    form = AlarmForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            alarm = Alarms.query.filter_by(order=form.order.data).first()
            if alarm:
                flash('Order exist')
                return redirect(url_for('pbx.alarm_index'))
            play_file = form.play_file.data
            order = form.order.data
            active = form.active.data
            alarm = Alarms(play_file=play_file, order=order, active=active)
            db.session.add(alarm)
            db.session.commit()
            flash("Alarm Inserted Successfully")
        else:
            flash("Wrong insert")

    return redirect(url_for('pbx.alarm_index'))


@bp.route('/alarm/update/<id>', methods=['GET','POST'])
@login_required
@admin_required
def alarm_update(id):
    form = AlarmForm()
    if request.method == 'POST':
        alarm = Alarms.query.filter_by(id=id).first_or_404()
        flash(form.active.data)
        alarm.play_file = form.play_file.data
        alarm.order = form.order.data
        alarm.active = form.active.data
        db.session.commit()
        flash("Alarm Updated Successfully")
        return redirect(url_for('pbx.alarm_index'))


# delete employee
@bp.route('/alarm/delete/<id>/', methods=['GET', 'POST'])
@admin_required
def alarm_delete(id):
    alarm = Alarms.query.get(id)
    db.session.delete(alarm)
    db.session.commit()
    flash("Alarm Deleted Successfully")
    return redirect(url_for('pbx.alarm_index'))