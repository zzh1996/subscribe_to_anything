from . import app
from flask_mail import Mail,Message

mail = Mail(app)

def send_confirm_mail(email):
    subject = 'Confirm code - Subscribe to anything'
    msg = Message(subject=subject, html='123456', recipients=[email])
    mail.send(msg)
