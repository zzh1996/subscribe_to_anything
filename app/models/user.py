from flask_login import UserMixin
from app import db, login_manager as lm


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(127), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    reg_token = db.Column(db.String(127))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def auth(cls, email, password):
        user = cls.query.filter(db.and_(User.email == email, User.password == password)).first()
        return user, user and user.active

    @classmethod
    def exist_user(cls, email):
        user = cls.query.filter(db.and_(User.email == email, User.active == True)).first()
        return bool(user)

    @classmethod
    def get_user_from_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user

    @classmethod
    def get_confirm_user(cls, code):
        user = cls.query.filter(db.and_(User.reg_token == code, User.active == False)).first()
        return user

    def save(self):
        db.session.add(self)
        db.session.commit()


@lm.user_loader
def load_user(userid):
    return User.query.get(userid)
