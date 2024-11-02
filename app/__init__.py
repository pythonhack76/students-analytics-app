from flask import Flask
from .database import init_db
import os

# Crea il percorso assoluto per il database
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'students.db')
INSTANCE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance')

# Assicurati che la directory instance esista
os.makedirs(INSTANCE_PATH, exist_ok=True)

app = Flask(__name__,
            template_folder=os.path.abspath('app/templates'),
            static_folder=os.path.abspath('app/static'),
            instance_path=INSTANCE_PATH)

# Configurazione
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializzazione del database
init_db(app)

# Importa le routes dopo l'inizializzazione del db
from app import routes
