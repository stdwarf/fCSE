from flask import render_template, flash, redirect, url_for, request, app
from app import db
from app.main.forms import CallforwardForm
from app.models import Callforward
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    form = CallforwardForm()
    callforward_data = Callforward.query.order_by(Callforward.exten).all()
    return render_template("index.html", callforward_data=callforward_data, form=form)


# insert data to mysql database via html forms
@bp.route('/insert', methods=['POST'])
def insert():
    form = CallforwardForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
#    if form.validate_on_submit():
        fwd = Callforward.query.filter_by(exten=form.exten.data).first()
        if fwd:
            flash('Callforward exist')
            return redirect(url_for('main.index'))
#          if request.method == 'POST':
        exten = form.exten.data
        forward_phone = form.forward_phone.data
        timeout = form.timeout.data
        my_data = Callforward(exten, forward_phone, timeout)
        print(my_data)
        db.session.add(my_data)
        db.session.commit()
        flash("Callforward Inserted Successfully")
    return redirect(url_for('main.index'))


# update employee
@bp.route('/update/<id>', methods=['POST'])
def update(id):
    form = CallforwardForm()
    if request.method == 'POST':
        my_data = Callforward.query.filter_by(id=id).first()
        print(my_data)
        my_data.exten = form.exten.data
        my_data.forward_phone = form.forward_phone.data
        my_data.timeout = form.timeout.data
        db.session.commit()
        flash("Callforward Updated Successfully")
        return redirect(url_for('main.index'))


# delete employee
@bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Callforward.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Callforward Deleted Successfully")
    return redirect(url_for('main.index'))
