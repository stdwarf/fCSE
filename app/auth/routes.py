from datetime import datetime

import ldap
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, request, flash, current_app, url_for, session
from werkzeug.urls import url_parse
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User, Role
from app.main.routes import get_ldap_connection
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
#        flash('You are already logged in.')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        conn = get_ldap_connection()
        usr = form.username.data+'@'+current_app.config['LDAP_HOST']
        pwd = form.password.data
        try:
            conn.simple_bind_s(usr, pwd)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('auth/login.html', form=form)
        except ldap.SERVER_DOWN:
            flash('AD server not available')
            return render_template('auth/login.html', form=form)
        try:
            username = form.username.data
            ldap_filter = f'sAMAccountName={username}'
            data = conn.search_s(current_app.config['LDAP_BASE_DN'], ldap.SCOPE_SUBTREE, ldap_filter,
                                 current_app.config['LDAP_FILTER'])
            email = data[0][1]['mail'][0].decode('utf-8')
            fullname = data[0][1]['displayName'][0].decode('utf-8')
            company = data[0][1]['company'][0].decode('utf-8')
            department = data[0][1]['department'][0].decode('utf-8')
            title = data[0][1]['title'][0].decode('utf-8')
            user = User.query.filter_by(username=username).first()
            if user is None:
                u = User(username=username, email=email, fullname=fullname, company=company, description=title, active=True)
                u.roles.append(Role.query.filter_by(name='User').first())
                db.session.add(u)
                db.session.commit()
            else:
                user.username = username
                user.email = email
                user.fullname = fullname
                user.company = company
                user.department = department
                user.description = title
                db.session.commit()
        except:
            db.session.rollback()
            flash("Something happen")
        conn.unbind_s()
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Something happen with login', 'fail')
        else:
            login_user(user, remember=True)
            session['last_active'] = datetime.now()
#            flash('You have successfully logged in.', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("auth/login.html", title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
