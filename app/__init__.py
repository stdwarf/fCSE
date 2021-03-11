# -*- coding: utf-8 -*-
import logging
from datetime import timedelta, datetime
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
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

from app import models

if __name__ == '__main__':
    app.run(host='172.17.200.13', port=6000, debug=True)