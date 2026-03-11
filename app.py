import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# Configuration de la page Streamlit
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Projet Machine Learning - EDA & Déploiement",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Fonctions de chargement des données et du modèle (à compléter par les étudiants)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    Fonction pour charger le dataset.
    Remplacez le code ci-dessous par la lecture de votre fichier de données Kaggle.
    Exemple: return pd.read_csv("data/raw/votre_fichier.csv")
    """
    # Données simulées pour l'exemple
    np.random.seed(42)
    df = pd.DataFrame({
        "Feature_1": np.random.randn(500),
        "Feature_2": np.random.rand(500) * 100,
        "Feature_3": np.random.randint(1, 5, 500),
        "Target": np.random.choice([0, 1], 500)
    })
    return df

@st.cache_resource
def load_model():
    """
    Fonction permettant de charger votre modèle pré-entraîné (ex: RandomForest).
    Exemple avec joblib :
    return joblib.load('models/mon_modele.pkl')
    """
    class DummyModel:
        def predict(self, X):
            return np.random.choice([0, 1], size=len(X))
        
        def predict_proba(self, X):
            proba = np.random.rand(len(X), 2)
            proba = proba / proba.sum(axis=1, keepdims=True)
            return proba

    return DummyModel()

# Chargement initial
try:
    df = load_data()
    model = load_model()
    data_loaded = True
except Exception as e:
    st.error(f"Erreur lors du chargement des données ou du modèle : {e}")
    data_loaded = False

# -----------------------------------------------------------------------------
# Menu de Navigation (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.title("Navigation")
menu = ["🏠 Accueil", "📊 Analyse Exploratoire (EDA)", "🤖 Test du Modèle", "💡 Conclusions & Perspectives"]
choice = st.sidebar.radio("Sommaire :", menu)

st.sidebar.markdown("---")

# Ajouter des fonctionnalités supplémentaires dans la sidebar (ex: filtres globaux)
if choice == "📊 Analyse Exploratoire (EDA)" and data_loaded:
    st.sidebar.subheader("Filtres Globaux")
    target_filter = st.sidebar.multiselect("Filtrer par Target :", options=df["Target"].unique(), default=df["Target"].unique())
    # Filtrer le dataframe
    df = df[df["Target"].isin(target_filter)]

st.sidebar.markdown("---")
st.sidebar.info("Template d'application Streamlit développé pour le projet Aflokkat.")

# =============================================================================
# Section 1 : Accueil
# =============================================================================
if choice == "🏠 Accueil":
    st.title("Projet Machine Learning : De l'Analyse au Déploiement 🎓")
    
    st.markdown("""
    Cette application Streamlit est un template robuste conçu pour présenter les résultats de votre modèle de Machine Learning basé sur un dataset (ex: Kaggle).
    """)
    
    # Utilisation de st.expander pour cacher/afficher l'information détaillée
    with st.expander("📌 Vos Missions (Étudiants) : Cliquez pour développer", expanded=True):
        st.markdown("""
        1. **Données** : Placer le vrai dataset dans le dossier `data/` et l'importer dans la fonction `load_data()`.
        2. **EDA** : Remplacer les visualisations génériques par vos propres graphiques interactifs (Plotly, Seaborn, Altair).
        3. **Modélisation** : Entraîner un modèle dans un notebook (dossier `notebooks/`), le sauvegarder (ex: avec `joblib` ou `pickle`) dans le dossier `models/`, et le charger dans `load_model()`.
        4. **Prédiction** : Créer un formulaire interactif robuste pour tester le modèle sur de nouvelles données.
        5. **Conclusion** : Rédiger un bilan clair et argumenté des performances et pistes d'amélioration.
        """)

    st.subheader("Structure du projet recommandée :")
    st.code("""
    mon_projet/
    ├── app.py                  # Script principal Streamlit (ce fichier)
    ├── requirements.txt        # Fichier des dépendances
    ├── README.md               # Documentation de votre projet
    ├── data/
    │   ├── raw/                # Données brutes de Kaggle
    │   └── processed/          # Données nettoyées (optionnel)
    ├── models/                 # Modèles entraînés (.pkl, .joblib, etc.)
    ├── notebooks/              # Vos notebooks d'exploration et d'entraînement (Jupyter)
    └── src/
        └── utils.py          # Fonctions ou classes python externes au script principal
    """, language="markdown")

# =============================================================================
# Section 2 : Analyse Exploratoire (EDA)
# =============================================================================
elif choice == "📊 Analyse Exploratoire (EDA)":
    st.title("Analyse Exploratoire des Données (EDA) 📈")
    
    if data_loaded:
        # Utilisation de st.tabs pour organiser finement l'affichage
        tab1, tab2, tab3 = st.tabs(["Aperçu des données", "Statistiques Descriptives", "Visualisations"])
        
        with tab1:
            st.subheader("Extrait du jeu de données")
            st.dataframe(df.head(15), use_container_width=True)
            
            # Bouton de téléchargement
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger le dataset filtré au format CSV",
                data=csv,
                file_name='dataset_filtre.csv',
                mime='text/csv',
            )
            
        with tab2:
            st.subheader("Description des variables")
            st.write(df.describe())
            
            # Affichage de métriques clés "Dashboard style"
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Nombre de lignes", df.shape[0])
            col_m2.metric("Nombre de colonnes", df.shape[1])
            col_m3.metric("Valeurs manquantes totales", df.isna().sum().sum())

        with tab3:
            st.subheader("Visualisations Graphiques")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Distribution de Feature_1 (selon la Target)**")
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.histplot(data=df, x="Feature_1", hue="Target", kde=True, ax=ax, palette="Set1")
                st.pyplot(fig)
                
            with col2:
                st.markdown("**Matrice de Corrélation**")
                fig, ax = plt.subplots(figsize=(6, 4))
                corr = df.select_dtypes(include=[np.number]).corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, fmt=".2f", vmin=-1, vmax=1)
                st.pyplot(fig)
                
            st.info("💡 **Astuce Étudiant :** Explorer le package `plotly.express` pour des graphiques 100% interactifs (zooms, survol, etc.).")

# =============================================================================
# Section 3 : Test du Modèle
# =============================================================================
elif choice == "🤖 Test du Modèle":
    st.title("Tester le Modèle de Machine Learning 🚀")
    st.markdown("""
    Testez la prédiction du modèle en modifiant les paramètres via le formulaire ci-dessous.
    """)
    
    with st.form("prediction_form"):
        st.subheader("Définissez les paramètres d'entrée :")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            feat_1 = st.number_input("Feature 1 (Valeur continue)", value=0.0, step=0.1)
        with col2:
            feat_2 = st.slider("Feature 2 (Curseur)", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
        with col3:
            feat_3 = st.selectbox("Feature 3 (Catégorie numérique)", options=[1, 2, 3, 4, 5])
            
        submit_button = st.form_submit_button(label="Exécuter le modèle")

    if submit_button:
        # Configuration des logs ou spin d'attente
        with st.spinner('Analyse par le modèle en cours...'):
            input_data = pd.DataFrame({
                "Feature_1": [feat_1], 
                "Feature_2": [feat_2],
                "Feature_3": [feat_3]
            })
            
            # Séparation de l'UI pour la réponse
            st.markdown("### Résultats")
            
            try:
                prediction = model.predict(input_data)
                proba = model.predict_proba(input_data)
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    if prediction[0] == 1:
                        st.success(f"La classe prédite est : **{prediction[0]}**")
                    else:
                        st.warning(f"La classe prédite est : **{prediction[0]}**")
                        
                with res_col2:
                    st.markdown("**Confiance du modèle (Probabilités)**")
                    proba_df = pd.DataFrame(proba, columns=["Classe 0", "Classe 1"]).T
                    st.bar_chart(proba_df)
                
            except Exception as e:
                st.error(f"Erreur lors de la prédiction. Vérifiez que les colonnes données au modèle correspondent exactement à celles attendues. Détail : {e}")

# =============================================================================
# Section 4 : Conclusions & Perspectives
# =============================================================================
elif choice == "💡 Conclusions & Perspectives":
    st.title("Conclusions et Pistes d'Amélioration 🎯")
    
    st.markdown("""
    ### 📝 Bilan du Projet
    Utilisez cette page pour résumer l'impact métier de votre modèle par rapport au problème Kaggle initial. 
    Parlez des compromis, de la précision vs le rappel de votre modèle (ex: importance des Faux Positifs).
    
    **Performances Finales du Modèle :**
    - **Accuracy :** 85% (exemple)
    - **F1-Score :** 82% (exemple)
    
    ### 🚧 Pistes d'Améliorations futures
    """)
    
    # Checklist des améliorations pour implémentation par les étudiants
    st.checkbox("✨ Ingénierie des caractéristiques avancées (Feature Engineering)")
    st.checkbox("🚀 Entraînement sur une infrastructure Cloud (AWS, GCP)")
    st.checkbox("🌍 Intégrer l'API FastAPI en backend plutôt que d'avoir le modèle directement dans Streamlit")
    st.checkbox("📈 Ajout d'explicabilité du modèle (SHAP values intégrées visuellement)")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Projet Streamlit Template par Baptiste Audroin | Aflokkat</p>", unsafe_allow_html=True)
