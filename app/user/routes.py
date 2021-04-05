from datetime import datetime

from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, request, flash, current_app, url_for, session
from app.user import bp
from app.user.forms import UserForm
from app.models import User, Role, UserRoles
from app import db, operator_required


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


@bp.route('/user')
@login_required
@operator_required
def user():
    form = UserForm()
    user_data = User.query.order_by(User.id).all()
    return render_template("user/user.html", user_data=user_data, form=form)


@bp.route('/update/<id>', methods=['POST'])
@login_required
@operator_required
def update(id):
    form = UserForm()
    if request.method == 'POST':
        my_data = UserRoles.query.filter_by(user_id=id).first()
        my_data.role_id = Role.query.filter_by(name=form.roles.data).first().id
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('user.user'))