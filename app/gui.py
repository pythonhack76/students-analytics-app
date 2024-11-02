import tkinter as tk
from tkinter import ttk
from .models import Student, Grade
from .database import db

class StudentEntryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Data Entry")
        
        # Create form fields
        ttk.Label(self.root, text="Student Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        
        ttk.Label(self.root, text="Subject:").grid(row=1, column=0)
        self.subject_entry = ttk.Entry(self.root)
        self.subject_entry.grid(row=1, column=1)
        
        ttk.Label(self.root, text="Score:").grid(row=2, column=0)
        self.score_entry = ttk.Entry(self.root)
        self.score_entry.grid(row=2, column=1)
        
        # Submit button
        ttk.Button(self.root, text="Submit", command=self.submit_data).grid(row=3, column=1)
    
    def submit_data(self):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        score = float(self.score_entry.get())
        
        student = Student.query.filter_by(name=name).first()
        if not student:
            student = Student(name=name)
            db.session.add(student)
            db.session.commit()
        
        grade = Grade(subject=subject, score=score, student_id=student.id)
        db.session.add(grade)
        db.session.commit()
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)