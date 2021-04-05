from flask import Blueprint

bp = Blueprint('pbx', __name__)

from app.pbx import routes