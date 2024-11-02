from flask import render_template, request, redirect, url_for, flash
from app import app
from .models import Student, Grade
from .database import db
from .analysis import DataAnalyzer

@app.route('/')
def dashboard():
    try:
        analyzer = DataAnalyzer()
        grade_distribution = analyzer.create_grade_distribution_plot()
        student_summary = analyzer.get_student_performance_summary()
        
        if student_summary.empty:
            flash('No student data available yet. Please add some students.', 'info')
            students_data = []
        else:
            students_data = student_summary.to_dict('records')
        
        return render_template('dashboard.html',
                             grade_distribution=grade_distribution,
                             students=students_data)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('dashboard.html', 
                             grade_distribution=None,
                             students=[])

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            subject = request.form.get('subject')
            score = float(request.form.get('score'))
            
            # Validazione
            if not name or not subject or score < 0 or score > 100:
                flash('Invalid input. Please check your data.', 'error')
                return redirect(url_for('add_student'))
            
            student = Student.query.filter_by(name=name).first()
            if not student:
                student = Student(name=name)
                db.session.add(student)
                db.session.commit()
            
            grade = Grade(subject=subject, score=score, student_id=student.id)
            db.session.add(grade)
            db.session.commit()
            
            flash('Student data added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('add_student'))
        
    return render_template('add_student.html')
