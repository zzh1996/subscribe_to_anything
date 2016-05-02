from flask_wtf import Form
from wtforms import (StringField, PasswordField, RadioField, IntegerField)
from wtforms.validators import (DataRequired,Email,EqualTo,URL,NumberRange)

class AddForm(Form):
    name=StringField('Name',validators=[DataRequired()])
    url=StringField('URL',validators=[DataRequired(),URL()])
    ua=StringField('User Agent')
    referer=StringField('Referer')
    cookie=StringField('Cookie')
    method=RadioField('Method',choices=[('GET','GET'),('POST','POST')])
    postdata=StringField('Post Data(json)')
    freq=IntegerField('Frequency(seconds)',validators=[DataRequired(),NumberRange(1,100000)])
    watch_type=RadioField('Send mail when',choices=[('change','Page changes'),('keyword','Keyword detected (Not supported yet)')])
    notify_content=RadioField('Mail content',choices=[('diff','Insertions and deletions (Diff)'),('new','New content'),('all','Entire new page')])

class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])

class RegisterForm(Form):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),
        EqualTo('confirm_password', message='passwords must match')])
    confirm_password = PasswordField('Confirm password')

class ConfirmForm(Form):
    code = StringField('Confirm code',validators=[DataRequired()])

