from .database import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name}>'

class Grade(db.Model):
    __tablename__ = 'grade'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return f'<Grade {self.subject}: {self.score}>'
