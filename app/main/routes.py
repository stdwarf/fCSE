import ldap
from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_login import login_required, logout_user
from flask_security import current_user, roles_accepted
from datetime import datetime, timedelta
from app import db
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

def get_ldap_connection():
    conn = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn

def make_session_permanent():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=5)



@bp.route('/')
def start():
    return redirect(url_for('auth.login'))


@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')
