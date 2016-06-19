from . import app
from flask_mail import Mail, Message
import sys

mail = Mail(app)


def send_mail(subject, body, email):
    with app.app_context():
        if app.config['MAIL_ENABLE']:
            msg = Message(subject=subject, body=body, recipients=[email])
            mail.send(msg)
        print('TO:', email, file=sys.stderr)
        print('Subject:', subject, file=sys.stderr)
        print('Body:', body, file=sys.stderr)
