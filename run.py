#!/usr/bin/env python3.4
# encoding: utf-8

from app import app
from app import db
from app.models import User,Page

if __name__ == '__main__':
    db.create_all()
    app.run(port=5000)

