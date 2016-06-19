from flask_login import UserMixin
from app import db
from app.daemon import *
import app
from .user import *
from datetime import datetime


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    postdata = db.Column(db.Text)
    ua = db.Column(db.Text)
    referer = db.Column(db.Text)
    cookie = db.Column(db.Text)
    method = db.Column(db.Enum('GET', 'POST'))
    watch_type = db.Column(db.Enum('change', 'keyword'))
    notify_content = db.Column(db.Enum('diff', 'new', 'all'))
    freq = db.Column(db.Integer)
    last_check = db.Column(db.DateTime)
    last_status = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref('pages'))

    def __init__(self, name, url, postdata, ua, referer, cookie, method, watch_type, notify_content, freq, user):
        self.name = name
        self.url = url
        self.postdata = postdata
        self.ua = ua
        self.referer = referer
        self.cookie = cookie
        self.method = method
        self.watch_type = watch_type
        self.notify_content = notify_content
        self.freq = freq
        self.user = user

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()
        app.dm.deletetask(self.id)
        app.dm.addtask(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        app.dm.deletetask(self.id)

    def update_check(self, status):
        page = self.query.get(self.id)
        if page:
            page.last_check = datetime.now()
            page.last_status = status
            db.session.add(page)
            db.session.commit()

    def email(self):
        return load_user(self.user_id).email
