# book-scraper-python

## P2 : Utilisez les bases de Python pour l'analyse de marché

Ce projet Python a été réalisé dans le cadre du Projet 2 du parcours **Développeur d'Applications Python** d'OpenClassrooms.

Il met en œuvre un programme de *web scraping* pour extraire des données tarifaires et des informations détaillées de la librairie fictive **Books to Scrape**. Les données sont ensuite structurées et exportées sous forme de fichiers **CSV**.

---

## ⚙️ Fonctionnalités du Scraper

Le programme `main.py` permet d'extraire des données de `https://books.toscrape.com/index.html` et d'enregistrer les informations détaillées (titre, prix, description, stock, etc.) dans un ou plusieurs fichiers **CSV** optimisés, ainsi que les images de couverture.

---

## 💻 Instructions d'Installation et d'Exécution

### Prérequis

* **Python 3** (version 3.6 ou supérieure recommandée)
* **Git**

### 1. Récupération du Projet

Naviguez vers le dossier souhaité, puis clonez le *repository* :

### 2 . Configuration de l'environnement virtuel

Système d'Exploitation      Commandes

Windows (Powershell)        python -m venv env .\env\Scripts\activate
MacOS / Linux (Terminal)    python3 -m venv env source env/bin/activate

 ### 3. Installation des Paquets Requis
Une fois l'environnement activé, installez les dépendances nécessaires (requests, beautifulsoup4, pandas, etc.) :

pip install -r requirements.txt

### 4. Lancement du Programme

Exécutez le script principal :

Système d'Exploitation  Commande  

Windows                 python main.py
MacOS / Linux           python3 main.py