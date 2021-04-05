# -*- coding: utf-8 -*-
import logging
from datetime import timedelta, datetime
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
from flask import Flask, session, flash, current_app, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
login.next_url = 'auth.login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.pbx import bp as pbx_bp
    app.register_blueprint(pbx_bp, url_prefix='/pbx')

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/fwd.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CSE startup')
    return app


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        flash(current_user.roles[0].name)
        if current_user.roles[0].name in current_app.config['ADMIN_ROLE_LIST']:
            return f(*args, **kwargs)
        else:
            flash("You need to be an Admin to view this page.")
            return redirect(url_for('main.index'))

    return wrap


def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        flash(current_user.roles[0].name)
        if current_user.roles[0].name in current_app.config['USER_ROLE_LIST']:
            return f(*args, **kwargs)
        else:
            flash("You need to be an User to view this page.")
            return redirect(url_for('main.index'))

    return wrap


def operator_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        flash(current_user.roles[0].name)
        if current_user.roles[0].name in current_app.config['OPERATOR_ROLE_LIST']:
            return f(*args, **kwargs)
        else:
            flash("You need to be an Operator to view this page.")
            return redirect(url_for('main.index'))

    return wrap



from app import models

if __name__ == '__main__':
    app.run(host='172.17.200.13', port=6000, debug=True)