import sqlite3
from sqlite3 import Error

def create_connection():
    try:
        conn = sqlite3.connect('students.db')
        return conn
    except Error as e:
        print(e)
    return None

def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                grade REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        conn.commit()
    except Error as e:
        print(e)

# app/models.py
class Student:
    def __init__(self, id, name, class_name):
        self.id = id
        self.name = name
        self.class_name = class_name

    @staticmethod
    def create(conn, name, class_name):
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, class) VALUES (?, ?)", 
                   (name, class_name))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def get_all(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        return cur.fetchall()

class Grade:
    def __init__(self, id, student_id, subject, grade, date):
        self.id = id
        self.student_id = student_id
        self.subject = subject
        self.grade = grade
        self.date = date

    @staticmethod
    def create(conn, student_id, subject, grade, date):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO grades (student_id, subject, grade, date)
            VALUES (?, ?, ?, ?)""", 
            (student_id, subject, grade, date))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def get_student_grades(conn, student_id):
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM grades 
            WHERE student_id = ?""", 
            (student_id,))
        return cur.fetchall()