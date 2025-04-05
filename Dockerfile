# Basis-Image
FROM python:3.11-slim

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Port 5001 für den Container freigeben
EXPOSE 5001

# Befehl zum Starten der Anwendung
CMD ["python", "app.py"]

