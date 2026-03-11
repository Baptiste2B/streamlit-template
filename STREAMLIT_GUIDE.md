# 📘 Le Grand Guide Streamlit : De Débutant à Expert pour votre Projet ML

Ce document exhaustif a pour but de recenser les composants, astuces, et bonnes pratiques incontournables de Streamlit. Il est pensé pour vous accompagner tout au long de votre projet d'Analyse de Données et de Machine Learning avec Aflokkat.

---

## 🏗️ 1. Architecture et Layout (Mise en page)

L'organisation visuelle de votre application est essentielle pour offrir une bonne expérience utilisateur (UX). Streamlit offre plusieurs outils pour structurer votre page.

### 1.1 Configurer la page (Toujours en haut du script)
```python
st.set_page_config(
    page_title="Mon Projet ML",
    page_icon="🤖", 
    layout="wide", # Peut être "centered" (défaut) ou "wide" (toute la largeur)
    initial_sidebar_state="expanded" # "auto", "expanded", "collapsed"
)
```

### 1.2 Structurer le contenu principal
- **Les Colonnes :** Créer des tableaux de bord (Dashboards).
  ```python
  # Créer 3 colonnes de taille égale
  col1, col2, col3 = st.columns(3)
  
  # Ou des colonnes avec des proportions différentes (ex: 70% et 30%)
  col_gauche, col_droite = st.columns([0.7, 0.3])
  
  with col_gauche:
      st.write("Texte principal à gauche")
  with col_droite:
      st.write("Aperçu à droite")
  ```

- **Les Onglets (Tabs) :** Idéal pour ne pas surcharger la page en hauteur (très utile dans l'EDA).
  ```python
  tab_data, tab_stats, tab_graphs = st.tabs(["Données", "Statistiques", "Visualisations"])
  with tab_data:
      st.dataframe(df)
  ```

- **Les Expanders (Panneaux dépliants) :** Pour cacher du texte ou des options avancées.
  ```python
  with st.expander("Voir les détails mathématiques du modèle"):
      st.write("Voici la formule de l'entropie croisée...")
      st.latex(r''' H(p, q) = -\sum_{x} p(x) \log q(x) ''') # Oui, Streamlit gère le LaTeX !
  ```

- **La Barre Latérale (Sidebar) :** L'endroit parfait pour la navigation et les filtres globaux.
  ```python
  # Tout élément st. peut être mis dans la sidebar avec st.sidebar
  st.sidebar.title("Paramètres Globaux")
  categorie = st.sidebar.selectbox("Choisissez une catégorie", ["A", "B", "C"])
  ```

---

## 📊 2. Affichage des Données et Métriques

### 2.1 Les DataFrames et Tableaux
- `st.dataframe(df, use_container_width=True)` : Affiche un tableau interactif (tri des colonnes, scroll, redimensionnement).
- `st.data_editor(df)` : Affiche un tableau *éditable*. L'utilisateur peut modifier les valeurs directement dans la page web (ex: corriger une faute de frappe) et récupérer le dataframe modifié.
- `st.table(df)` : Affiche un tableau statique, plus "propre" visuellement, mais très lent si vous avez plus de 50 lignes.

### 2.2 Les Métriques (Type "Dashboard")
L'élément `st.metric` est parfait pour mettre en évidence les KPIs de votre modèle.
```python
col1, col2, col3 = st.columns(3)
col1.metric(label="Accuracy du Modèle", value="85.4%", delta="2.1%") # delta positif = flèche verte
col2.metric(label="RMSE", value="12.3", delta="-1.5", delta_color="inverse") # delta_color="inverse" : pour une erreur, une baisse (négatif) est une bonne chose (flèche verte)
col3.metric(label="Temps d'inférence", value="45 ms")
```

---

## 🎛️ 3. Interactivité : Les "Widgets" (Inputs Utilisateurs)

Chaque fois que l'utilisateur modifie un widget, **tout le script Python est ré-exécuté de haut en bas**.

### 3.1 Saisies basiques
```python
# Texte
nom = st.text_input("Votre nom", value="Jean Dupont")
mot_de_passe = st.text_input("Mot de passe", type="password")
message = st.text_area("Laissez un commentaire")

# Nombres
age = st.number_input("Âge", min_value=0, max_value=120, value=25, step=1)
taille = st.slider("Taille (cm)", 100.0, 220.0, 175.0, 0.5)
```

### 3.2 Choix multiples et booléens
```python
accepter = st.checkbox("J'accepte les conditions")

# Choix unique
genre = st.radio("Sélectionnez le genre", ["Homme", "Femme", "Autre"], horizontal=True)
pays = st.selectbox("Pays d'origine", ["France", "Belgique", "Suisse", "Canada"])

# Choix multiples (Renvoie une LISTE des options choisies)
langages = st.multiselect("Langages de programmation connus", ["Python", "R", "SQL", "Java", "C++"])
```

### 3.3 Import & Export de fichiers
```python
# Uploader un fichier CSV
fichier_charge = st.file_uploader("Chargez vos propres données Kaggle", type=["csv", "xlsx"])
if fichier_charge is not None:
    df = pd.read_csv(fichier_charge)

# Proposer un fichier au téléchargement
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger le fichier traité",
    data=csv,
    file_name="donnees_propres.csv",
    mime="text/csv"
)
```

---

## 🎨 4. Intégration de Graphiques (Visualisations)

Évitez `st.pyplot(fig)` (Matplotlib/Seaborn) si possible, car les graphiques sont statiques (des simples images). 
Privilégiez **Plotly** ou **Altair** pour avoir des graphiques interactifs où l'utilisateur peut zoomer et survoler les points.

### 4.1 Plotly Express (Recommandé)
```python
import plotly.express as px

# Nuage de points
fig_scatter = px.scatter(df, x="Feature_1", y="Feature_2", color="Target", hover_data=["Feature_3"])
st.plotly_chart(fig_scatter, use_container_width=True)

# Histogramme
fig_hist = px.histogram(df, x="Feature_1", color="Target", barmode="overlay")
st.plotly_chart(fig_hist, use_container_width=True)
```

### 4.2 Altair (Excellente alternative)
```python
import altair as alt

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Feature_1',
    y='Feature_2',
    color='Target:N',
    tooltip=['Feature_1', 'Feature_2', 'Target']
).interactive()

st.altair_chart(chart, use_container_width=True)
```

---

## ⚡ 5. L'Art de l'Optimisation (CRITIQUE pour le ML)

Comme Streamlit recharge la page en entier à chaque clic, vous DEVEZ bloquer les exécutions longues (lecture de gros CSV, entraînement de modèles) pour qu'elles n'aient lieu qu'une seule fois. C'est le rôle de **la mise en cache**.

### 5.1 `@st.cache_data` (Pour les données)
Utilisez ce décorateur au-dessus des fonctions qui renvoient des DataFrames ou des variables basiques.

```python
@st.cache_data
def charger_donnees_brutes(chemin):
    """Sera exécuté la première fois. Les fois suivantes, Streamlit lira la RAM."""
    return pd.read_csv(chemin)

df = charger_donnees_brutes("data/raw/dataset.csv")
```

### 5.2 `@st.cache_resource` (Pour les modèles ML ou les connexions BDD)
Utilisez ce décorateur pour tout objet Python complexe qui ne peut pas être converti en texte brut (comme un modèle scikit-learn, XGBoost, TensorFlow, ou une connexion via psycopg2/SQLAlchemy).

```python
@st.cache_resource
def charger_modele_ml():
    import joblib
    # Le modèle lourd de 500Mo ne sera chargé qu'une seule fois en RAM
    return joblib.load("models/random_forest_final.pkl")

modele = charger_modele_ml()
```

### 5.3 Les Formulaires (`st.form`)
Si vous avez 5 curseurs (sliders) sur votre page de prédiction de modèle, changer la valeur d'un seul curseur va recharger toute l'application et lancer une prédiction inutile.
**Le formulaire met les inputs "en pause"** jusqu'à ce que l'utilisateur clique sur "Valider".

```python
with st.form(key="formulaire_prediction"):
    col1, col2 = st.columns(2)
    poid = col1.number_input("Poids (kg)")
    taille = col2.number_input("Taille (cm)")
    fumeur = st.checkbox("Fumeur ?")
    
    # Le bouton de soumission est OBLIGATOIRE dans un form
    bouton_soumission = st.form_submit_button(label="Prédire le risque")

# L'action ne se déclenche que si le bouton a été pressé
if bouton_soumission:
    risque = modele.predict([[poid, taille, fumeur]])
    st.write(f"Le résultat est : {risque}")
```

---

## 💬 6. Messages à l'Utilisateur et Esthétique

Streamlit propose des boîtes de dialogue natives très élégantes pour informer l'utilisateur de ce qu'il se passe.

```python
st.success("Opération réussie avec succès ! 🎉")
st.info("Information : Le modèle a été entraîné sur 50 000 lignes.")
st.warning("Attention : Vous tentez de prédire une valeur avec des données manquantes.")
st.error("Erreur critique : Fichier modèle introuvable.")
```

### Indicateurs d'état de chargement
Lorsqu'une prédiction ou le traitement d'un fichier prend beaucoup de temps.
```python
import time

with st.spinner('Chargement du modèle de Deep Learning en cours... Veuillez patienter.'):
    time.sleep(3) # Simule une tâche de 3 secondes
    st.success('Modèle prêt !')
```

```python
# Barre de progression
barre = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    barre.progress(i + 1, text=f"Traitement : {i+1}%")
```

---

## 🔐 7. État de Session (Session State) : Le "Mode Avancé"

La mémoire basique de Streamlit se perd à chaque clic. 
Si vous voulez stocker une variable qui "survit" aux rechargements de la page (ex: un compteur de clics, le nom de l'utilisateur connecté, ou un historique de prédictions), vous devez utiliser la `st.session_state`.

```python
# Initialiser la variable si elle n'existe pas encore
if 'compteur' not in st.session_state:
    st.session_state['compteur'] = 0

# Créer un bouton qui incrémente le compteur
if st.button("Cliquez-moi !"):
    st.session_state['compteur'] += 1

st.write(f"Vous avez cliqué {st.session_state['compteur']} fois.")
```

*Avec toutes ces connaissances, vous êtes prêts à construire des Dashboards dignes de Data Scientists professionnels ! Bon courage ! 🚀*
