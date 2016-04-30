from flask import Blueprint,render_template,redirect,url_for
from flask.ext.login import current_user,login_required

home = Blueprint('home',__name__)

@home.route('/')
@login_required
def index():
    return redirect(url_for('manage.index'))

