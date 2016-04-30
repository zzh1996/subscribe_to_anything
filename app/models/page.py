from flask.ext.login import UserMixin
from app import db

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    postdata = db.Column(db.Text)
    ua = db.Column(db.Text)
    referer = db.Column(db.Text)
    cookie = db.Column(db.Text)
    method = db.Column(db.Enum('GET','POST'))
    watch_type = db.Column(db.Enum('change','keyword'))
    notify_content = db.Column(db.Enum('diff','new','all'))
    freq = db.Column(db.Integer)
    user = db.relationship('User',backref=db.backref('pages'))


