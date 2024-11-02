from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Crea il contesto dell'applicazione
    with app.app_context():
        # Importa i modelli qui per evitare importazioni circolari
        from .models import Student, Grade
        
        # Crea tutte le tabelle
        db.create_all()
        
        # Verifica se le tabelle sono state create
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelle create nel database: {tables}")