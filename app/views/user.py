from flask import Blueprint,render_template,redirect,url_for,request
from flask.ext.login import login_user,current_user,login_required
from app.forms import LoginForm
from app.models import *

user= Blueprint('user',__name__)

@user.route('/login/',methods=['POST','GET'])
def login():
    next_url = request.args.get('next') or url_for('home.index')
    if current_user.is_authenticated:
        return redirect(next_url)
    form = LoginForm()
    error=''
    if request.method == 'POST':
        if form.validate_on_submit():
            user,status=User.auth(form['email'].data,form['password'].data)
            if status:
                login_user(user)
                return redirect(next_url)
            else:
                error='email or password incorrect'
        else:
            error='invalid form data'
    return render_template('login.html',form=form,error=error)
