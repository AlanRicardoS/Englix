from flask_sqlalchemy import SQLAlchemy

from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return '<name %r, email %r, password %r, id %r>' % (self.name, self.email, self.password, self.id)
