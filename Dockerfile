# Utiliser une image Python officielle comme base
FROM python:3.12.2

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir tkinter sqlite3

# Exposer le port que l'application utilisera
EXPOSE 4000

# Lancer l'application
CMD ["python", "app.py"]
