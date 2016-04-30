from flask.ext.login import UserMixin
from app import db,login_manager as lm

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(127),unique=True)
    password = db.Column(db.String(127),nullable=False)
    active = db.Column(db.Boolean(), default=False)
    reg_token = db.Column(db.String(127))

    def __init__(self,email,password):
        self.email=email
        self.password=password

    @classmethod
    def auth(cls,email,password):
        user = cls.query.filter(db.and_(User.email==email,User.password==password)).first()
        return user,user and user.active

@lm.user_loader
def load_user(userid):
        return User.query.get(userid)
