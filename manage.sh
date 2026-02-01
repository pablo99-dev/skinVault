#!/bin/bash

# Appliquer les migrations (changes)

echo "Application des migrations..."
python3 manage.py migrate
