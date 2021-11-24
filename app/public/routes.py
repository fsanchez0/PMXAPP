from flask import render_template
from flask_login import login_required

from . import public_bp

@public_bp.route('/')
@login_required
def home():
    return render_template('public/index.html')