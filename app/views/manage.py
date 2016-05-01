from flask import Blueprint,render_template,redirect,url_for,request,Response
from flask.ext.login import current_user,login_required
from app.forms import *
from app.models import *
from app.mail import *
from app import db
from app.download import *

manage= Blueprint('manage',__name__)

@manage.route('/')
@login_required
def index():
    pages=current_user.pages
    return render_template('manage.html',user=current_user,pages=pages)

@manage.route('/add/',methods=['POST','GET'])
@login_required
def add():
    form=AddForm()
    error=''
    if request.method == 'POST':
        if form.validate_on_submit():
            page=Page(form['name'].data,
                      form['url'].data,
                      form['postdata'].data,
                      form['ua'].data,
                      form['referer'].data,
                      form['cookie'].data,
                      form['method'].data,
                      form['watch_type'].data,
                      form['notify_content'].data,
                      form['freq'].data,
                      current_user
                      )
            page.save()
            return redirect(url_for('manage.index'))
    return render_template('add.html',form=form,error=error)

@manage.route('/delete/<int:id>')
@login_required
def delete(id):
    page=Page.query.get(id)
    if not page or page.user!=current_user:
        return redirect(url_for('manage.index'))
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for('manage.index'))

@manage.route('/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit(id):
    error=''
    page=Page.query.get(id)
    if not page or page.user!=current_user:
        return redirect(url_for('manage.index'))
    form=AddForm(request.form,page)
    if request.method == 'POST':
        if form.validate_on_submit():
            page.name=form['name'].data
            page.url=form['url'].data
            page.postdata=form['postdata'].data
            page.ua=form['ua'].data
            page.referer=form['referer'].data
            page.cookie=form['cookie'].data
            page.method=form['method'].data
            page.watch_type=form['watch_type'].data
            page.notify_content=form['notify_content'].data
            page.freq=form['freq'].data
            page.save()
            return redirect(url_for('manage.index'))
    return render_template('edit.html',form=form,error=error,id=page.id)

@manage.route('/test/<int:id>',methods=['POST','GET'])
@login_required
def test(id):
    page=Page.query.get(id)
    if not page or page.user!=current_user:
        return redirect(url_for('manage.index'))
    try:
        text=download(page.url,page.ua,page.referer,page.cookie,page.method,page.postdata)
    except Exception as e:
        text=type(e).__name__
    return Response(text,mimetype='text/plain')


