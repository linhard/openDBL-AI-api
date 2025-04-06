# Basisimage
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode und .env-Datei kopieren
COPY app.py .
COPY .env .

# Port freigeben
EXPOSE 5001

# Startkommando
CMD ["python", "app.py"]

