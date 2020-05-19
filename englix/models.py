from flask_sqlalchemy import SQLAlchemy
import enum

from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<name %r, email %r, password %r, id %r>' % (self.name, self.email, self.password, self.id)

class LevelType(enum.Enum):
    Intermadiate = 30
    Advanced = 60
    Fluent = 80

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_type = db.Column(db.Enum(LevelType))

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    activities = db.relationship('Activity', backref='lesson', cascade="all,delete", lazy=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    
    quizes = db.relationship('Quiz', backref='activity', cascade="all,delete", lazy=True)

class QuizType(enum.Enum):
    Video = "Video"
    AR = "AR"
    Text = "Text"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_type = db.Column(db.Enum(QuizType))
    #conteúdo dependendo do  tipo de quiz: texto, video ou foto AR
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    
    answers = db.relationship('Answer', backref='quiz', cascade="all,delete", lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
