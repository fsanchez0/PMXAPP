from flask import Blueprint

asistencias_bp = Blueprint('asistencias', __name__, template_folder='templates')

from . import routes