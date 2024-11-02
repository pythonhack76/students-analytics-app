FROM python:3.9-slim

# Installa le dipendenze del sistema
RUN apt-get update && apt-get install -y \
    tk-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Espone la porta per Flask
EXPOSE 5000

CMD ["python", "run.py"]