import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .database import db

class DataAnalyzer:
    @staticmethod
    def create_grade_distribution_plot():
        try:
            # Query grades from database
            grades_df = pd.read_sql('SELECT score FROM grade', db.engine)
            
            if grades_df.empty:
                # Se non ci sono dati, crea un grafico vuoto
                plt.figure(figsize=(10, 6))
                plt.title('Grade Distribution (No data available)')
            else:
                plt.figure(figsize=(10, 6))
                sns.histplot(data=grades_df, x='score', bins=20)
                plt.title('Grade Distribution')
            
            # Save plot to bytes buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close()  # Chiude la figura per liberare memoria
            
            return base64.b64encode(image_png).decode()
        except Exception as e:
            print(f"Error in create_grade_distribution_plot: {str(e)}")
            return None

    @staticmethod
    def get_student_performance_summary():
        try:
            query = """
            SELECT student.name, 
                   AVG(grade.score) as avg_score,
                   COUNT(grade.id) as total_grades
            FROM student
            JOIN grade ON student.id = grade.student_id
            GROUP BY student.id, student.name
            """
            df = pd.read_sql(query, db.engine)
            return df
        except Exception as e:
            print(f"Error in get_student_performance_summary: {str(e)}")
            return pd.DataFrame()
