from flask import Blueprint

evaluaciones_bp = Blueprint('evaluaciones', __name__, template_folder='templates')

from . import routes