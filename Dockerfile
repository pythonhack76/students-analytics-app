FROM python:3.9-slim

# Crea un utente non-root
RUN useradd -m appuser

WORKDIR /app

# Copia i file necessari
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Crea le directory necessarie e imposta i permessi
RUN mkdir -p instance && \
    mkdir -p app/templates app/static/css app/static/js && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/instance

# Passa all'utente non-root
USER appuser

EXPOSE 5000

CMD ["python", "run.py"]