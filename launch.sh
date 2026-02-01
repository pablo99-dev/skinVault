#!/bin/bash
# Script de lancement Django
#verifiez que vous avez bien modifier le fichier /config/settings.py (ajout des info de la bdd)

#ouverture de page 
xdg-open http://localhost:8000/login/ & 


# Lancer le serveur
echo "Lancement du serveur..."
python3 manage.py runserver  


