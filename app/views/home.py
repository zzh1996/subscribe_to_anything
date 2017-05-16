from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

home = Blueprint('home', __name__)


@home.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    return redirect(url_for('manage.index'))
