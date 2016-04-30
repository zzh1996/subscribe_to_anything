from flask import Blueprint,render_template,redirect,url_for,request
from flask.ext.login import login_user,current_user,login_required,logout_user
from app.forms import *
from app.models import *
from random import randint
from app import db
from app.mail import *

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
            error='please input email and password'
    return render_template('login.html',form=form,error=error)

@user.route('/register/',methods=['POST','GET'])
def register():
    form = RegisterForm()
    error=''
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.exist_user(form['email'].data):
                error='user already exists'
            else:
                user=User.get_user_from_email(form['email'].data)
                if not user:
                    user=User(form['email'].data,form['password'].data)
                code=str(randint(100000,999999))
                user.reg_token=code
                user.save()
                send_mail('Confirm code',code,form['email'].data)
                return redirect(url_for('user.confirm'))
        else:
            error='email not valid or password not match'
    return render_template('register.html',form=form,error=error)

@user.route('/confirm/',methods=['POST','GET'])
def confirm():
    form = ConfirmForm()
    error=''
    if request.method == 'POST':
        if form.validate_on_submit():
            user=User.get_confirm_user(form['code'].data)
            if user:
                user.active=True
                user.save()
                login_user(user)
                return redirect(url_for('home.index'))
            else:
                error='wrong code'
        else:
            error='please input confirm code'
    return render_template('confirm.html',form=form,error=error)

@user.route('/logout/')
def logout():
    logout_user();
    return redirect(url_for('home.index'));


