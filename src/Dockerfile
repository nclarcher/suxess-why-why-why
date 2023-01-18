FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source https://github.com/jkleinlercher/suxess-why-why-why

# Erstelle Arbeitsverzeichnis
RUN mkdir /app
WORKDIR /app

# Kopiere die Anwendung in das Arbeitsverzeichnis
COPY . .

# Installiere die Abhängigkeiten
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Öffne Port 5000
EXPOSE 5000

# Starte die Anwendung
CMD ["python", "app.py"]

