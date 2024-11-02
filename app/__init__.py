from flask import Flask
from app.database import create_connection, create_tables

def create_app():
    app = Flask(__name__)
    
    # Inizializza il database
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        conn.close()
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app

# app/routes.py
from flask import Blueprint, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from app.database import create_connection
from app.models import Student, Grade

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/student_performance')
def student_performance():
    conn = create_connection()
    
    # Ottieni tutti i voti
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name, g.subject, g.grade, g.date
        FROM students s
        JOIN grades g ON s.id = g.student_id
    """)
    
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['student', 'subject', 'grade', 'date'])
    
    # Crea grafici
    graphs = {}
    
    # Media voti per studente
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='student', y='grade')
    plt.xticks(rotation=45)
    plt.title('Media Voti per Studente')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    graphs['avg_grades'] = base64.b64encode(buf.getvalue()).decode()
    plt.close()
    
    # Media voti per materia
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='subject', y='grade')
    plt.xticks(rotation=45)
    plt.title('Distribuzione Voti per Materia')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    graphs['subject_dist'] = base64.b64encode(buf.getvalue()).decode()
    plt.close()
    
    # Statistiche generali
    stats = {
        'total_students': len(df['student'].unique()),
        'total_grades': len(df),
        'avg_grade': df['grade'].mean(),
        'best_subject': df.groupby('subject')['grade'].mean().idxmax(),
    }
    
    conn.close()
    return jsonify({'graphs': graphs, 'stats': stats})

# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)