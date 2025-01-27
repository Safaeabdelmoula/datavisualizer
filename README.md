# **Data Visualizer**

*Application web de visualisation et d'analyse statistique de données développée avec Django.*


##  **Fonctionnalités Principales**

- **Téléchargement de fichiers CSV**
- **Affichage des statistiques descriptives (moyenne, variance,écart-type, min, max)**
- **Visualisation graphique des données numériques**


## **Technologies Utilisées**
- **Backend:**Django
- **Frontend :** HTML ,CSS
- **Analyse des Données:**Pandas
- **Visualisation :** Matplotlib, Seaborn  
- **Base de Données :** SQLite (par défaut de Django)  

###  **Installation du Projet**

1. **Clonez le repository:**

```bash 
clone https://github.com/safae04/data_visualizer.git
cd data-visualizer 
```

2. **Créez un environnement virtuel :**
   ```
   python -m venv venv
   venv\Scripts\activate     # Sur Windows
   ```

3. **Installez les dépendances :**
   ```
   pip install -r requirements.txt
   ```

4. **Appliquez les migrations de la base de données :**
   ```
   python manage.py migrate
   ```

5. **Lancez le serveur :**
   ```
   python manage.py runserver
   ```

*Accédez au projet via [http://localhost:8000](http://localhost:8000).*


**Structure du projet**


datavisualizer/
├── dataapp/                   # Application principale Django
│   ├── templates/             # Fichiers HTML
│   │   ├── upload.html
│   │   ├── index.html
│   │   ├── stats.html
│   │   ├── visualize.html
│   ├── static/
│   ├── views.py               # Logique métier
│   ├── models.py              # Modèles de données
│   ├── urls.py                # Routes
├── datavisualizer/
│   ├── settings.py
│   ├── urls.py                # Routes principaux
└── manage.py

## **Utilisation**
1. Téléversez un fichier CSV via l'interface d'upload.  
2. Consultez les **statistiques** après le traitement du fichier.  
3. Accédez aux **visualisations graphiques**.  
