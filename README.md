# Template Streamlit - Projet Machine Learning Aflokkat

Ce dépôt est un **template de base** développé par Baptiste Audroin pour Aflokkat, destiné aux étudiants souhaitant mettre en valeur leur projet d'analyse exploratoire des données (EDA) et de modélisation Machine Learning sous forme d'application web interactive.

## Structure du Projet (Arborescence)

Une fois configuré, un bon projet d'analyse et de modélisation doit se rapprocher de l'architecture suivante :

```text
streamlit_aflokkat/
│
├── app.py                  # Script principal Streamlit (Le cœur de l'application)
├── requirements.txt        # Fichier listant l'ensemble des dépendances (librairies)
├── README.md               # Ce fichier d'explication
│
├── data/
│   ├── raw/                # Les datasets bruts téléchargés depuis Kaggle
│   └── processed/          # Les datasets après nettoyage et feature engineering
│
├── models/                 # Les modèles de Machine Learning sauvegardés (ex: avec joblib, format .pkl)
│
├── notebooks/              # Les notebooks Jupyter (.ipynb) utilisés pour l'exploration de données et l'entraînement du modèle
│
└── src/                    # (Optionnel) Scripts Python complémentaires (fonctions d'entraînement, nettoyage)
    └── utils.py
```

## Les Dépendances (Requirements)

Les bibliothèques utilisées dans ce template sont :
- `streamlit` : Le framework utilisé pour créer l'interface web en Python.
- `pandas` & `numpy` : Pour la manipulation et le calcul de données sous forme de DataFrames.
- `matplotlib` & `seaborn` : Pour générer des visualisations graphiques avancées.
- `pillow` (PIL) : Pour gérer l'affichage d'images dans l'interface (si nécessaire).

> Pensez à ajouter d'autres bibliothèques dans `requirements.txt` selon vos besoins, comme `scikit-learn`, `xgboost`, ou `plotly`.

## 🛠️ Instructions d'Installation et d'Utilisation

Pour faire fonctionner cette application sur votre machine de manière propre et isolée des autres projets, il est impératif d'utiliser un **environnement virtuel**.

### Étape 1 : Créer et activer l'environnement virtuel (.venv)

Ouvrez un terminal et naviguez dans le dossier du projet.

**Sur Windows :**
```bash
# 1. Créer l'environnement virtuel nommé ".venv"
python -m venv .venv

# 2. Activer l'environnement virtuel
.venv\Scripts\activate
```

**Sur macOS et Linux :**
```bash
# 1. Créer l'environnement virtuel nommé ".venv"
python3 -m venv .venv

# 2. Activer l'environnement virtuel
source .venv/bin/activate
```
*(Vous verrez `.venv` affiché au début de la ligne de votre terminal, ce qui indique que l'environnement est actif).*

### Étape 2 : Installer les dépendances

Alors que votre environnement virtuel est actif, installez toutes les bibliothèques nécessaires au bon fonctionnement de l'application :

```bash
pip install -r requirements.txt
```

### Étape 3 : Lancer l'Application Streamlit

Pour démarrer l'application locale, exécutez la commande suivante :

```bash
streamlit run app.py
```

Votre navigateur va alors s'ouvrir automatiquement (ou vous pouvez cliquer sur le lien `http://localhost:8501` affiché dans votre terminal) sur votre Dashboard interactif. 🎉

---
**Rappel de Développement :** À chaque modification du fichier `app.py`, sauvegardez le fichier, et l'application proposera en haut à droite un bouton `Rerun` ou `Always Rerun` pour mettre à jour l'affichage instantanément.
