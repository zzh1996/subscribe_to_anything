from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, URL, NumberRange
from app import app


class AddForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    ua = StringField('User Agent')
    referer = StringField('Referer')
    cookie = StringField('Cookie')
    method = SelectField('Method', choices=[('GET', 'GET'), ('POST', 'POST')])
    postdata = StringField('Post Data(json)')
    if app.config['FREQ_SECOND']:
        unit = '(seconds)'
    else:
        unit = '(minutes)'
    freq = IntegerField('Frequency' + unit, validators=[DataRequired(), NumberRange(1, 100000)])
    watch_type = SelectField('Send mail when',
                            choices=[('change', 'Page changes'), ('keyword', 'Keyword detected (Not supported yet)')])
    notify_content = SelectField('Mail content',
                                choices=[('diff', 'Insertions and deletions (Diff)'), ('new', 'New content'),
                                         ('all', 'Entire new page')])
    submit_btn = SubmitField('Submit')
