# 🚗 IFRI GO - Plateforme de Covoiturage Étudiante

**Projet universitaire** visant à créer une plateforme web de covoiturage pour les étudiants de l’IFRI (UAC).

---

## 📝 Description

**IFRI GO** est une plateforme développée avec **Django + MySQL** permettant :
- la publication de trajets,
- la réservation de places,
- l’échange de messages privés,
- et la gestion de profil.

Ce projet facilite la mise en relation entre conducteurs et passagers de la communauté universitaire.

---

## ⚙️ Prérequis

- Python 3.13
- MySQL installé localement
- `pip` et `venv` installés
- Dépendances Python :
  - asgiref==3.8.1
  - Django==5.2.3
  - mysqlclient==2.2.7
  - pillow==11.2.1
  - sqlparse==0.5.3
  - tzdata==2025.2

---

## 🚀 Installation

### 1. Cloner le projet

git clone <URL_du_projet>

cd IFRI_GO

### 2. Créer un environnement virtuel et l’activer

Sur Windows :

python -m venv env

.\env\Scripts\activate

Sur Linux / macOS :

python3 -m venv env

source env/bin/activate

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Configuration de la base de données

Créez une base MySQL avec le nom de votre choix :

CREATE DATABASE ifri_go;

Dans backend/settings.py, modifiez la section DATABASES :

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'ifri_go',

        'USER': 'root',

        'PASSWORD': '',

        'HOST': 'localhost',

        'PORT': '3306',

    }

}
📝 Modifiez USER et PASSWORD selon votre configuration MySQL.

### 5. Migrations

Dans le dossier back-end/ :

cd back-end 

python manage.py migrate

### 6. Creer un super utilisateur (admin)

python manage.py createsuperuser

### 7. Lancer le serveur

python manage.py runserver

Puis ouvrez :

http://127.0.0.1:8000/

### 8. Fonctionnalités principales

✅ Création/suppression de trajets par les conducteurs

✅ Publication d’annonces à partir de ses trajets

✅ Réservation de trajets (hors trajets créés par soi-même)

✅ Notification pour les conducteurs lors d’une réservation

✅ Inscription / connexion utilisateur

✅ Messagerie privée entre utilisateurs

✅ Boîte de réception + historique des messages

✅ Modification du profil

✅ Feedback visuel (messages de confirmation ou erreur)

### 9. Organisation du projet

backend/ → Code Django

backend/settings.py → Configuration

user/, covoiturage/ → Apps

frontend/pages/ → Versions indépendantes des templates

templates/ → Templates utilisés par Django

avec Mysql sur votre ordinateur , les bases de données seront automatiquement generer

### 10. Remarques importantes

N’oubliez pas d’adapter vos identifiants MySQL.

En production, pensez à masquer votre SECRET_KEY et à utiliser un fichier .env.

Le projet est en cours d’évolution. Contributions bienvenues.

Merci d’utiliser IFRI GO !
Bon covoiturage 🚗✨
