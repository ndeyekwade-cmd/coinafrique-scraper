# 🐾 CoinAfrique Animal Scraper

Application web de scraping des annonces d'animaux sur CoinAfrique.com avec interface Streamlit moderne.

## 📋 Description

Cette application permet de scraper automatiquement les annonces d'animaux sur CoinAfrique.com pour 4 catégories:
- 🐕 Chiens
- 🐑 Moutons
- 🐔 Poules, Lapins et Pigeons
- 🐾 Autres Animaux

## ✨ Fonctionnalités

- ✅ Scraping automatique avec Selenium et BeautifulSoup
- ✅ Nettoyage automatique des données (suppression des doublons et valeurs nulles)
- ✅ Visualisations interactives (top adresses, distribution des prix)
- ✅ Interface moderne avec design inspiré de Tailwind CSS
- ✅ Export des données en CSV et Excel
- ✅ Suivi en temps réel avec barre de progression
- ✅ Statistiques détaillées

## 🚀 Installation locale

### Prérequis
- Python 3.8+
- Chrome ou Chromium installé
- ChromeDriver

### Installation

```bash
# Cloner le repository
git clone <votre-repo-url>
cd Final_exam_ndeye_khady_wade

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app_streamlit.py
```

## 🌐 Déploiement sur Streamlit Cloud

1. Poussez ce repository sur GitHub
2. Allez sur [Streamlit Cloud](https://streamlit.io/cloud)
3. Connectez votre compte GitHub
4. Sélectionnez ce repository
5. Le fichier principal est `app_streamlit.py`
6. Déployez!

## 📁 Structure du projet

```
Final_exam_ndeye_khady_wade/
│
├── app_streamlit.py              # Application Streamlit principale
├── requirements.txt              # Dépendances Python
├── packages.txt                  # Packages système (pour Streamlit Cloud)
├── .gitignore                    # Fichiers à ignorer par Git
├── README.md                     # Documentation
│
└── Partie1_scrapping_using_beautifulSoup.ipynb  # Notebook Jupyter
```

## 💡 Utilisation

1. Sélectionnez une catégorie dans la barre latérale
2. Choisissez le nombre de pages à scraper (1-50)
3. Cliquez sur "🚀 Lancer le scraping"
4. Visualisez les résultats dans les onglets:
   - 📊 **Visualisations**: Graphiques d'analyse
   - 📋 **Données**: Tableau des données scrapées
   - 💾 **Export**: Télécharger en CSV ou Excel

## 📊 Données collectées

Pour chaque annonce:
- **Name/Details**: Nom ou description de l'animal
- **Price**: Prix en CFA
- **Address**: Localisation
- **Image Link**: URL de l'image

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **Streamlit**: Framework web
- **Selenium**: Scraping automatisé
- **BeautifulSoup**: Parsing HTML
- **Pandas**: Manipulation de données
- **Matplotlib**: Visualisations
- **openpyxl**: Export Excel

## 👨‍💻 Auteur

**Ndeye Khady Wade**
AIMS Senegal - Data Collection Project

## 📝 Licence

Ce projet est à usage éducatif dans le cadre du programme AIMS Senegal.

## ⚠️ Avertissement

Cette application est destinée à des fins éducatives uniquement. Veuillez respecter les conditions d'utilisation de CoinAfrique.com et ne pas surcharger leurs serveurs.
