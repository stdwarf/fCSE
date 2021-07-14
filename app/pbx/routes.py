import json
from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, session, current_app, jsonify
from flask_login import login_required, logout_user
from flask_security import current_user, roles_accepted
from app import db, time
from app.main.forms import CallforwardForm
from app.models import Clid, Ps_auths, Ps_aors, Ps_endpoints, Alarms, Callforward, Blacklist
from app.pbx import bp
from app.pbx.forms import ClidForm, ExtenForm, AlarmForm, BlacklistForm

@bp.app_template_filter('formatdatetime')
def format_datetime(value, format="%d-%m-%Y %H:%M:%S "):
    if value is None:
        return ""
    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')
    return value.strftime(format)

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

@bp.route('/fwd/index')
@roles_accepted('Admin', 'Operator','User')
def fwd_index():
    form = CallforwardForm()
    callforward_data = Callforward.query.order_by(Callforward.exten).all()
    return render_template("pbx/fwd.html", callforward_data=callforward_data, form=form)


# insert data to mysql database via html forms
@bp.route('/fwd/insert', methods=['POST'])
@roles_accepted('Admin', 'Operator')
def fwd_insert():
    form = CallforwardForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        fwd = Callforward.query.filter_by(exten=form.exten.data).first()
        if fwd:
            flash('Callforward exist')
            return redirect(url_for('pbx.fwd_index'))
#          if request.method == 'POST':
        exten = form.exten.data
        forward_phone = form.forward_phone.data
        timeout = form.timeout.data
        ticket = form.ticket.data
        owner = current_user.fullname
        history = f"{exten},{forward_phone},{timeout},{ticket},{owner},{time};"
        callforward = Callforward(exten=exten, forward_phone=forward_phone, timeout=timeout, ticket=ticket, owner=owner, history=history)
        db.session.add(callforward)
        db.session.commit()
        flash("Callforward Inserted Successfully")
      else:
        flash("Wrong insert")

    return redirect(url_for('pbx.fwd_index'))


# update Callforward
@bp.route('/fwd/update/<id>', methods=['POST'])
@roles_accepted('Admin', 'Operator')
def fwd_update(id):
    form = CallforwardForm()
    if request.method == 'POST':
        callforward = Callforward.query.filter_by(id=id).first_or_404()
        callforward.exten = form.exten.data
        callforward.forward_phone = form.forward_phone.data
        callforward.timeout = form.timeout.data
        callforward.ticket = form.ticket.data
        callforward.owner = current_user.fullname
        b_list = callforward.history.split(';')
        if len(b_list) > 4:
                del b_list[0]
                b_str = ';'.join([str(item) for item in b_list])
                callforward.history = f"{b_str}{form.exten.data},{form.forward_phone.data},{form.timeout.data},{form.ticket.data},{current_user.fullname},{time};"
        else:
            callforward.history = f"{callforward.history}{form.exten.data},{form.forward_phone.data},{form.timeout.data},{form.ticket.data},{current_user.fullname},{time};"
        db.session.commit()
        flash("Callforward Updated Successfully")
        return redirect(url_for('pbx.fwd_index'))


# delete Callforward
@bp.route('/fwd/delete/<id>/', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def fwd_delete(id):
    callforward = Callforward.query.get(id)
    db.session.delete(callforward)
    db.session.commit()
    flash("Callforward Deleted Successfully")
    return redirect(url_for('pbx.fwd_index'))


@bp.route('/clid/index')
@roles_accepted('Admin', 'Operator')
def clid_index():
    form = ClidForm()
    clid_data = Clid.query.order_by(Clid.clid_num).all()
    return render_template("pbx/clid.html", clid_data=clid_data, form=form)


@bp.route('/clid/update/<id>', methods=['POST'])
@roles_accepted('Admin', 'Operator')
def clid_update(id):
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
        return redirect(url_for('pbx.clid_index'))


# delete employee
@bp.route('/clid/delete/<id>/', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def clid_delete(id):
    my_data = Clid.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Clid Deleted Successfully")
    return redirect(url_for('pbx.clid_index'))


#exten
@bp.route('/exten/index')
@roles_accepted('Admin', 'Operator')
def exten_index():
    form = ExtenForm()
    exten = Ps_auths.query.order_by(Ps_auths.id).all()
    return render_template("pbx/exten.html", exten_data=exten, form=form)


# insert data to mysql database via html forms
@bp.route('/exten/insert', methods=['POST'])
@roles_accepted('Admin', 'Operator')
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
@roles_accepted('Admin', 'Operator')
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
@roles_accepted('Admin', 'Operator')
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
@roles_accepted('Admin', 'Operator')
def alarm_index():
    form = AlarmForm()
    alarm_data = Alarms.query.order_by(Alarms.order).all()
    return render_template("pbx/alarm.html", alarm_data=alarm_data, form=form)


@bp.route('/alarm/insert', methods=['POST'])
@roles_accepted('Admin', 'Operator')
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
@roles_accepted('Admin', 'Operator')
def alarm_update(id):
    form = AlarmForm()
    if request.method == 'POST':
        alarm = Alarms.query.filter_by(id=id).first_or_404()
        alarm.play_file = form.play_file.data
        alarm.order = form.order.data
        alarm.active = form.active.data
        db.session.commit()
        flash("Alarm Updated Successfully")
        return redirect(url_for('pbx.alarm_index'))


# delete employee
@bp.route('/alarm/delete/<id>/', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def alarm_delete(id):
    alarm = Alarms.query.get(id)
    db.session.delete(alarm)
    db.session.commit()
    flash("Alarm Deleted Successfully")
    return redirect(url_for('pbx.alarm_index'))


@bp.route('/alarm/postactive', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def alarm_postactive():
    dict=request.form.to_dict()
    activeid=dict['javascript_data[activeid]']
    active=dict['javascript_data[active]']
    if active=='true':
        active = True
    else:
        active = False
    print(active)
    print(activeid)
    if request.method == 'POST':
        alarm = Alarms.query.filter_by(id=activeid).first_or_404()
        alarm.active = active
        db.session.commit()
        flash("Alarm Updated Successfully")
    return redirect(url_for('pbx.alarm_index'))



@bp.route('/blacklist/index')
@roles_accepted('Admin', 'Operator')
def blacklist_index():
    form = BlacklistForm()
    blacklist_data = Blacklist.query.order_by(Blacklist.clid).all()
    return render_template("pbx/blacklist.html", blacklist_data=blacklist_data, form=form)


@bp.route('/blacklist/insert', methods=['POST'])
@roles_accepted('Admin', 'Operator')
def blacklist_insert():
    form = BlacklistForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            blacklist = Blacklist.query.filter_by(clid=form.clid.data).first()
            if blacklist:
                flash('Order exist')
                return redirect(url_for('pbx.blacklist_index'))
            clid = form.clid.data
            ticket = form.ticket.data
            active = form.active.data
            owner = current_user.fullname
            history = f"{clid},{ticket},{active},{owner},{time};"
            blacklist = Blacklist(clid=clid, ticket=ticket, owner=owner, active=active, history=history)
            db.session.add(blacklist)
            db.session.commit()
            flash("Blacklist Inserted Successfully")
        else:
            flash("Wrong insert")

    return redirect(url_for('pbx.blacklist_index'))


@bp.route('/blacklist/update/<id>', methods=['GET','POST'])
@roles_accepted('Admin', 'Operator')
def blacklist_update(id):
    form = BlacklistForm()
    if request.method == 'POST':
        blacklist = Blacklist.query.filter_by(id=id).first_or_404()
        blacklist.clid = form.clid.data
        blacklist.ticket = form.ticket.data
        blacklist.active = form.active.data
        blacklist.owner = current_user.fullname
        b_list = blacklist.history.split(';')
        if len(b_list) > 4:
                del b_list[0]
                b_str = ';'.join([str(item) for item in b_list])
                blacklist.history = f"{b_str}{form.clid.data},{form.ticket.data},{form.active.data},{current_user.fullname},{time};"
        else:
            blacklist.history = f"{blacklist.history}{form.clid.data},{form.ticket.data},{form.active.data},{current_user.fullname},{time};"
        db.session.commit()
        flash("Blacklist Updated Successfully")
        return redirect(url_for('pbx.blacklist_index'))


# delete
@bp.route('/blacklist/delete/<id>/', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def blacklist_delete(id):
    blacklist = Blacklist.query.get(id)
    db.session.delete(blacklist)
    db.session.commit()
    flash("Blacklist Deleted Successfully")
    return redirect(url_for('pbx.blacklist_index'))


@bp.route('/blacklist/postactive', methods=['GET', 'POST'])
@roles_accepted('Admin', 'Operator')
def blacklist_postactive():
    dict = request.form.to_dict()
    activeid = dict['javascript_data[activeid]']
    active = dict['javascript_data[active]']
    if active =='true':
        active = True
    else:
        active = False
    print(active)
    print(activeid)
    if request.method == 'POST':
        blacklist = Blacklist.query.filter_by(id=activeid).first_or_404()
        blacklist.active = active
        b_list = blacklist.history.split(';')
        if len(b_list) > 4:
                del b_list[0]
                b_str = ';'.join([str(item) for item in b_list])
                blacklist.history = f"{b_str}{blacklist.clid},{blacklist.ticket},{blacklist.active},{current_user.fullname},{time};"
        else:
            blacklist.history = f"{blacklist.history}{blacklist.clid},{blacklist.ticket},{blacklist.active},{current_user.fullname},{time};"
        db.session.commit()
        flash("Blacklist Updated Successfully")
    return redirect(url_for('pbx.blacklist_index'))