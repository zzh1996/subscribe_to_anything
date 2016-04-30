from flask import Blueprint,render_template,redirect,url_for
from flask.ext.login import current_user,login_required
from app.models import *
from app.mail import *

manage= Blueprint('manage',__name__)

@manage.route('/')
@login_required
def index():
    pages=current_user.pages
    return render_template('manage.html',user=current_user,pages=pages)

@manage.route('/add/')
@login_required
def add():
    send_confirm_mail('')


@manage.route('/delete/<int:id>')
@login_required
def delete():
    pass

@manage.route('/edit/<int:id>')
@login_required
def edit():
    pass


