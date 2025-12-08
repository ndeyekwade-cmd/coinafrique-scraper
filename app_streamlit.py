import streamlit as st
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import time

# Configuration de la page
st.set_page_config(
    page_title="CoinAfrique Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# Charger le CSS personnalisé
def local_css():
    st.markdown("""
    <style>
        /* Variables de couleurs */
        :root {
            --primary-blue: #0083B8;
            --accent-red: #F71938;
            --aims-red: #8B1538;
            --night-blue: #0f1419;
            --dark-blue: #1a1f2e;
            --text-dark: #070505;
            --text-light: #e8e8e8;
            --gray-light: #cecdcd;
            --white: #FFFFFF;
        }

        /* Masquer les éléments par défaut */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Background bleu nuit */
        .stApp {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        }

        /* Contenu principal - décaler pour le sidebar */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }

        /* Sidebar - Forcer la visibilité */
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            background-color: #1a1f2e;
            border-right: 1px solid rgba(0,131,184,0.2);
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            width: 21rem !important;
            height: 100vh;
            overflow-y: auto;
            z-index: 999999 !important;
        }

        /* Bouton pour ouvrir/fermer le sidebar */
        [data-testid="collapsedControl"] {
            display: block !important;
            visibility: visible !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-light) !important;
        }

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--primary-blue) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }

        /* Metric containers avec ombres colorées */
        [data-testid=metric-container] {
            background: rgba(26, 31, 46, 0.8);
            border: 1px solid rgba(0,131,184,0.3);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(247,25,56,0.4);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        [data-testid=metric-container]:hover {
            box-shadow: 0 0 20px rgba(247,25,56,0.6);
            transform: translateY(-3px);
            border-color: rgba(0,131,184,0.5);
        }

        [data-testid="metric-container"] > label {
            color: var(--text-light) !important;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
        }

        [data-testid="metric-container"] > div {
            color: var(--primary-blue) !important;
            font-size: 2rem;
            font-weight: 700;
        }

        /* Plot containers */
        .plot-container>div {
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 10px;
            background-color: rgba(26, 31, 46, 0.9);
            border: 1px solid rgba(0,131,184,0.2);
        }

        /* Boutons */
        .stButton>button {
            background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-red) 100%);
            color: white;
            border: none;
            padding: 0.75rem 2.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stButton>button:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }

        /* Selectbox et NumberInput */
        .stSelectbox, .stNumberInput {
            margin-bottom: 1.5rem;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(to right, #99ff99, #FFFF00);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(26, 31, 46, 0.9) !important;
            border: 1px solid rgba(0,131,184,0.3) !important;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            color: var(--text-light) !important;
            font-weight: 600;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(26, 31, 46, 1) !important;
            border-color: rgba(0,131,184,0.5) !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-red) 100%) !important;
            color: white !important;
            border-color: transparent !important;
        }

        /* DataFrame */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            border: 1px solid rgba(0,131,184,0.2);
        }

        /* Curseur pointer pour les selectbox */
        div[data-baseweb="select"],
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] > div,
        div[data-testid="stSelectbox"] > div > div {
            cursor: pointer !important;
        }

        /* Curseur pointer pour les options du menu déroulant */
        div[role="listbox"],
        div[role="option"] {
            cursor: pointer !important;
        }

        /* Titres */
        h1, h2, h3 {
            color: var(--text-light) !important;
            font-weight: 700;
        }

        /* Alert boxes */
        .alert-info {
            background: rgba(0, 131, 184, 0.15);
            border-left: 4px solid var(--primary-blue);
            padding: 2rem;
            border-radius: 8px;
            margin: 2rem auto;
            color: var(--text-light);
            border: 1px solid rgba(0,131,184,0.3);
            max-width: 800px;
        }

        .alert-info strong {
            display: block;
            text-align: center;
            margin-bottom: 1rem;
        }

        .alert-info b {
            display: block;
            text-align: left;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        .alert-success {
            background: rgba(40, 167, 69, 0.15);
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: var(--text-light);
            border: 1px solid rgba(40,167,69,0.3);
        }

        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-red) 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .section-header h2 {
            margin: 0;
            color: white !important;
            font-size: 1.5rem;
        }

        /* Footer */
        .custom-footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 2px solid rgba(0,131,184,0.3);
            color: var(--text-light);
        }

        p, span, label, div {
            color: var(--text-light);
        }

        /* Animations Accueil */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px rgba(0,131,184,0.5); }
            50% { text-shadow: 0 0 20px rgba(247,25,56,0.8), 0 0 30px rgba(0,131,184,0.5); }
        }

        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            padding: 2rem;
        }

        .welcome-title {
            font-size: 4rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-blue), var(--accent-red));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            text-align: center;
            animation: fadeInDown 1s ease-out, glow 3s ease-in-out infinite;
        }

        .welcome-subtitle {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            text-align: center;
            animation: fadeInUp 1.2s ease-out;
            opacity: 0;
            animation-fill-mode: forwards;
            animation-delay: 0.3s;
        }

        .welcome-btn-wrapper {
            animation: fadeInUp 1.4s ease-out;
            opacity: 0;
            animation-fill-mode: forwards;
            animation-delay: 0.6s;
        }

        .welcome-btn-wrapper .stButton>button {
            padding: 0.7rem 2rem;
            font-size: 1rem;
            width: 100%;
            animation: pulse 2s ease-in-out infinite;
            animation-delay: 1.5s;
        }

        .instructions-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            animation: fadeIn 0.8s ease-out;
        }

        .instruction-card {
            background: rgba(26, 31, 46, 0.8);
            border: 1px solid rgba(0,131,184,0.3);
            border-radius: 12px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }

        .instruction-card:hover {
            transform: translateX(10px);
            border-color: rgba(0,131,184,0.6);
            box-shadow: 0 6px 20px rgba(247,25,56,0.3);
        }

        .instruction-number {
            display: inline-block;
            width: 40px;
            height: 40px;
            line-height: 40px;
            text-align: center;
            background: linear-gradient(135deg, var(--primary-blue), var(--accent-red));
            border-radius: 50%;
            color: white;
            font-weight: 700;
            font-size: 1.2rem;
            margin-right: 1rem;
        }

    </style>
    """, unsafe_allow_html=True)

local_css()

# Fonction de scraping
@st.cache_data
def scraper_categorie(categorie_name, url, max_pages, selector_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")

    try:
        driver = webdriver.Chrome(options=options)
    except:
        options.binary_location = "/usr/bin/chromium"
        driver = webdriver.Chrome(options=options)

    data = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for p in range(0, max_pages):
        status_text.text(f"📥 Scraping page {p+1}/{max_pages}...")
        progress_bar.progress((p + 1) / max_pages)

        page_url = f'{url}?page={p}'
        driver.get(page_url)
        soup = bs(driver.page_source, 'html.parser')
        containers = soup.find_all('div', 'col s6 m4 l3')

        if not containers:
            break

        for container in containers:
            try:
                if selector_name == 'card-content':
                    name = container.find('div', class_='card-content ad__card-content')
                else:
                    name = container.find('p', class_='ad__card-description')
                name = name.text.strip() if name else None

                price = container.find('p', class_='ad__card-price')
                price = price.text.strip() if price else None

                address = container.find('p', class_='ad__card-location')
                address = address.span.text.strip() if address and address.span else None

                img_tag = container.find('img')
                image_link = img_tag.get('src', '') if img_tag else None

                data.append({
                    'name': name,
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except:
                pass

    driver.quit()
    progress_bar.empty()
    status_text.empty()

    df = pd.DataFrame(data)
    df = df.dropna(how='all')
    df = df.drop_duplicates(subset=['name', 'price', 'address'], keep='first')

    return df

# Fonction de visualisation
def visualiser_donnees(df, categorie_name):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'ANALYSE DES DONNÉES - {categorie_name}', fontsize=16, fontweight='bold', color='#e8e8e8')
    fig.patch.set_facecolor('#1a1f2e')

    if 'address' in df.columns and df['address'].notna().sum() > 0:
        top_addresses = df['address'].value_counts().head(10)
        axes[0].barh(range(len(top_addresses)), top_addresses.values, color='#0083B8')
        axes[0].set_yticks(range(len(top_addresses)))
        axes[0].set_yticklabels(top_addresses.index, fontsize=9, color='#e8e8e8')
        axes[0].set_xlabel('Nombre d\'annonces', fontweight='bold', color='#e8e8e8')
        axes[0].set_title('Top 10 des adresses', fontweight='bold', color='#e8e8e8')
        axes[0].invert_yaxis()
        axes[0].grid(axis='x', alpha=0.3, color='#cecdcd')
        axes[0].set_facecolor('#1a1f2e')
        axes[0].tick_params(colors='#e8e8e8')

    if 'price' in df.columns:
        df_temp = df.copy()
        df_temp['price_num'] = df_temp['price'].str.extract(r'(\d+)').astype(float)
        prices_valid = df_temp['price_num'].dropna()

        if len(prices_valid) > 0:
            axes[1].hist(prices_valid, bins=20, color='#F71938', edgecolor='black', alpha=0.7)
            axes[1].set_xlabel('Prix (CFA)', fontweight='bold', color='#e8e8e8')
            axes[1].set_ylabel('Fréquence', fontweight='bold', color='#e8e8e8')
            axes[1].set_title('Distribution des prix', fontweight='bold', color='#e8e8e8')
            axes[1].grid(axis='y', alpha=0.3, color='#cecdcd')
            axes[1].set_facecolor('#1a1f2e')
            axes[1].tick_params(colors='#e8e8e8')

            mean_price = prices_valid.mean()
            median_price = prices_valid.median()
            axes[1].axvline(mean_price, color='#0083B8', linestyle='--', linewidth=2, label=f'Moyenne: {mean_price:,.0f} CFA')
            axes[1].axvline(median_price, color='orange', linestyle='--', linewidth=2, label=f'Médiane: {median_price:,.0f} CFA')
            legend = axes[1].legend()
            for text in legend.get_texts():
                text.set_color('#e8e8e8')

    plt.tight_layout()
    return fig

# ==================== PAGE WELCOME ====================
if st.session_state.page == 'welcome':
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

    st.markdown("""
        <h1 class="welcome-title">📊 CoinAfrique Analytics</h1>
        <p class="welcome-subtitle">Plateforme d'analyse et de collecte de données</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-btn-wrapper">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("→ VISITER", key="welcome_btn"):
            st.session_state.page = 'instructions'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE INSTRUCTIONS ====================
elif st.session_state.page == 'instructions':
    st.markdown("""
    <div class="section-header">
        <h2>Guide d'utilisation</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="instructions-container">', unsafe_allow_html=True)

    # Introduction
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Bienvenue sur CoinAfrique Analytics</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                Cette plateforme vous permet de collecter et analyser automatiquement les données
                des annonces d'animaux publiées sur CoinAfrique Sénégal. L'outil extrait les informations
                clés (nom, prix, localisation, images) et génère des visualisations pour faciliter votre analyse.
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <strong style="color: #F71938;">Deux options s'offrent à vous :</strong><br>
                <span style="color: #0083B8;">•</span> Charger des données déjà collectées (3479 annonces disponibles)<br>
                <span style="color: #0083B8;">•</span> Scraper de nouvelles données en temps réel
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Option 1 - Données pré-collectées
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Option 1 : Charger des données pré-collectées</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                <strong>Accès immédiat à 3479 annonces déjà collectées</strong>
            </p>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li><strong>Chiens :</strong> 860 annonces</li>
                <li><strong>Moutons :</strong> 1324 annonces</li>
                <li><strong>Lapins/Poules/Pigeons :</strong> 804 annonces</li>
                <li><strong>Autres Animaux :</strong> 491 annonces</li>
            </ul>
            <p style="margin-top: 1rem; line-height: 1.6;">
                Dans le menu latéral, section "Données pré-collectées", sélectionnez la catégorie
                souhaitée et cliquez sur "CHARGER LES DONNÉES". Les visualisations s'afficheront
                instantanément sans attendre.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Option 2 - Scraper de nouvelles données
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Option 2 : Scraper de nouvelles données</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                <strong>Collectez des données fraîches en temps réel</strong>
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">1</span>
                <strong>Choisir une catégorie :</strong> Sélectionnez parmi Chiens, Moutons,
                Poules/Lapins/Pigeons, ou Autres Animaux dans le menu "Scraper de nouvelles données".
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">2</span>
                <strong>Définir le volume :</strong> Indiquez le nombre de pages (1-50).
                Environ 20 annonces par page. 5 pages = ~100 annonces, 20 pages = ~400 annonces.
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">3</span>
                <strong>Lancer le scraping :</strong> Cliquez sur "LANCER". Une barre de progression
                suivra l'avancement. Durée : quelques minutes selon le volume.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Analyse et export
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Analyser et exporter vos données</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                Une fois les données chargées ou scrapées, vous accédez à :
            </p>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li><strong>Indicateurs clés :</strong> Total annonces, prix, adresses, images, complétude</li>
                <li><strong>Visualisations :</strong> Top 10 des adresses, distribution des prix avec moyenne/médiane</li>
                <li><strong>Tableau de données :</strong> Consultation détaillée de toutes les annonces</li>
                <li><strong>Export :</strong> Téléchargement au format CSV ou Excel</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Conseils d'utilisation
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #F71938; margin-top: 0;">Conseils d'utilisation</h3>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li>Commencez avec les données pré-collectées pour une découverte rapide</li>
                <li>Pour du scraping, débutez avec 5-10 pages pour tester</li>
                <li>Les données scrapées sont mises en cache pour éviter les collectes répétées</li>
                <li>Utilisez le menu latéral pour basculer entre chargement et scraping</li>
                <li>Les graphiques peuvent être sauvegardés via clic droit</li>
                <li>Vérifiez l'indicateur de complétude avant l'export</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br><br>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("COMMENCER", key="start_scraping_btn"):
            st.session_state.page = 'scraping'
            st.rerun()

# ==================== PAGE SCRAPING ====================
elif st.session_state.page == 'scraping':

    # ========== HEADER ==========
    st.markdown("""
    <style>
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-blue), var(--accent-red));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-top: 0;
            margin-bottom: 0.3rem;
            animation: fadeInDown 1s ease-out, glow 3s ease-in-out infinite;
        }

        .dashboard-subtitle {
            color: #e8e8e8;
            font-size: 1.1rem;
            text-align: center;
            margin-top: 0;
            margin-bottom: 1rem;
            animation: fadeInUp 1.2s ease-out;
            opacity: 0;
            animation-fill-mode: forwards;
            animation-delay: 0.3s;
        }

        /* Réduire l'espace en haut de la page */
        .main > div:first-child {
            padding-top: 1rem !important;
        }
    </style>

    <h1 class="dashboard-title">Bienvenue sur votre Dashboard</h1>
    <p class="dashboard-subtitle">Utilisez le menu à gauche pour commencer</p>
    """, unsafe_allow_html=True)

    # Style simple pour séparation uniquement
    st.markdown("""
    <style>
        /* Barre de séparation entre les colonnes */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
            border-right: 4px solid #0083B8 !important;
            padding-right: 1rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
            padding-left: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Créer 2 colonnes: menu à gauche (limité), contenu à droite (large)
    col_menu, col_content = st.columns([0.7, 3.3])

    with col_menu:
        # Style global pour la colonne menu
        st.markdown("""
        <style>
            /* Cibler spécifiquement la première colonne du dashboard */
            section[data-testid="stVerticalBlock"] > div:has(button[key="load_data_btn"]) {
                background: linear-gradient(135deg, rgba(10, 15, 20, 0.95) 0%, rgba(20, 25, 35, 0.95) 100%) !important;
                padding: 1.5rem !important;
                border-radius: 8px !important;
                min-height: 70vh !important;
            }

            /* Réduire TOUS les espaces dans le menu de gauche */

            /* Expanders compacts */
            div[data-testid="stExpander"] {
                margin-bottom: 0.3rem !important;
                margin-top: 0 !important;
            }

            /* Contenu des expanders très compact */
            div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
                padding: 0.3rem 0.5rem !important;
            }

            /* TOUS les éléments verticaux dans expanders - gap minimal */
            div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
            div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"],
            div[data-testid="stExpander"] .element-container {
                gap: 0 !important;
                margin: 0 !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Selectbox - aucun espace */
            div[data-testid="stExpander"] div[data-testid="stSelectbox"],
            div[data-testid="stExpander"] div[data-baseweb="select"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Labels - aucun espace */
            div[data-testid="stExpander"] label {
                margin: 0 !important;
                padding: 0 !important;
                padding-bottom: 0.2rem !important;
                font-size: 0.85rem !important;
            }

            /* Number input - aucun espace */
            div[data-testid="stExpander"] div[data-testid="stNumberInput"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Text area - aucun espace */
            div[data-testid="stExpander"] div[data-testid="stTextArea"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Boutons - aucun espace au-dessus */
            div[data-testid="stExpander"] div[data-testid="stButton"],
            div[data-testid="stExpander"] button {
                margin-top: 0 !important;
                margin-bottom: 0.2rem !important;
                padding: 0.3rem 1rem !important;
            }

            /* Forcer les éléments à se coller */
            div[data-testid="stExpander"] .stSelectbox + div,
            div[data-testid="stExpander"] .stNumberInput + div,
            div[data-testid="stExpander"] .stTextArea + div {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }

            /* Supprimer les espaces entre widgets */
            div[data-testid="column"]:first-child [data-testid="stVerticalBlock"] {
                gap: 0 !important;
            }

            div[data-testid="column"]:first-child .element-container {
                margin-bottom: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Données pré-collectées
        with st.expander("📂 Données", expanded=True):

            datasets_disponibles = {
                "Chiens (860 annonces)": "chiens.csv",
                "Moutons (1324 annonces)": "moutons.csv",
                "Lapins/Poules/Pigeons (804 annonces)": "lapins_poules_pigeons.csv",
                "Autres Animaux (491 annonces)": "autres_animaux.csv"
            }

            dataset_choisi = st.selectbox(
                "Catégorie:",
                list(datasets_disponibles.keys()),
                key="dataset_select"
            )

            if st.button("CHARGER", use_container_width=True, key="load_data_btn"):
                try:
                    fichier = datasets_disponibles[dataset_choisi]
                    df = pd.read_csv(fichier, encoding='utf-8-sig')

                    # Renommer les colonnes pour avoir des noms cohérents
                    rename_map = {}
                    if 'adress' in df.columns:
                        rename_map['adress'] = 'address'
                    if 'location' in df.columns:
                        rename_map['location'] = 'address'
                    if 'img_link' in df.columns:
                        rename_map['img_link'] = 'image_link'
                    if 'image' in df.columns:
                        rename_map['image'] = 'image_link'

                    if rename_map:
                        df = df.rename(columns=rename_map)

                    # Garder TOUTES les colonnes du CSV
                    st.session_state['df'] = df
                    st.session_state['categorie'] = dataset_choisi.split(' (')[0]
                    st.session_state['show_feedback'] = False
                    st.success(f"✅ {len(df)} annonces chargées!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors du chargement: {str(e)}")

        with st.expander("🔍 Scraper", expanded=False):
            categories = {
                "🐕 Chiens": {
                    "url": "https://sn.coinafrique.com/categorie/chiens",
                    "selector": "card-content"
                },
                "🐑 Moutons": {
                    "url": "https://sn.coinafrique.com/categorie/moutons",
                    "selector": "description"
                },
                "🐔 Poules, Lapins et Pigeons": {
                    "url": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
                    "selector": "description"
                },
                "🐾 Autres Animaux": {
                    "url": "https://sn.coinafrique.com/categorie/autres-animaux",
                    "selector": "description"
                }
            }

            categorie_selectionnee = st.selectbox(
                "Catégorie:",
                list(categories.keys()),
                key="cat_select"
            )

            nb_pages = st.number_input(
                "Pages:",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
                key="nb_pages_input"
            )

            scraper_btn = st.button("LANCER", use_container_width=True, key="scrape_btn")

        with st.expander("💬 Feedback", expanded=False):
            if st.button("CHOISIR", use_container_width=True, key="feedback_btn"):
                st.session_state['show_feedback'] = True
                st.rerun()

    # ========== ZONE PRINCIPALE DU DASHBOARD (colonne droite) ==========
    with col_content:
        # Style global pour la colonne contenu
        st.markdown("""
        <style>
            /* Cibler la zone de contenu */
            div[data-testid="stVerticalBlock"] div[data-testid="column"]:last-child > div {
                background: linear-gradient(135deg, rgba(35, 40, 50, 0.5) 0%, rgba(30, 35, 45, 0.5) 100%) !important;
                padding: 1.5rem !important;
                border-radius: 8px !important;
                min-height: 70vh !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Affichage des cartes de feedback
        if 'show_feedback' in st.session_state and st.session_state['show_feedback']:
            st.markdown("""
            <div class="section-header">
                <h2>💬 Donnez votre avis</h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #0083B8 0%, #006a94 100%);
                    padding: 2rem;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 0 15px rgba(0, 131, 184, 0.4);
                    border: 1px solid rgba(0, 131, 184, 0.3);
                    height: 250px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📋</div>
                    <h3 style="color: white; margin-bottom: 1rem;">Google Form</h3>
                    <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem;">
                        Partagez votre expérience avec notre formulaire Google
                    </p>
                    <a href="https://docs.google.com/forms/d/e/1FAIpQLSeiYro0Of1uGx7A4rHP4jLP7Thmf7cWXGcWcp1DqdwgFxKf_g/viewform?usp=header" target="_blank">
                        <button style="
                            padding: 0.75rem 2rem;
                            background-color: white;
                            color: #0083B8;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 1rem;
                            font-weight: 600;
                            transition: all 0.3s;
                        ">
                            Ouvrir le formulaire
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #D946A6 0%, #8B1E5C 100%);
                    padding: 2rem;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 0 15px rgba(217, 70, 166, 0.4);
                    border: 1px solid rgba(217, 70, 166, 0.3);
                    height: 250px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                    <h3 style="color: white; margin-bottom: 1rem;">KoboToolbox</h3>
                    <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem;">
                        Répondez à notre enquête sur KoboToolbox
                    </p>
                    <a href="https://ee.kobotoolbox.org/x/LxX0vuSU" target="_blank">
                        <button style="
                            padding: 0.75rem 2rem;
                            background-color: white;
                            color: #D946A6;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 1rem;
                            font-weight: 600;
                            transition: all 0.3s;
                        ">
                            Ouvrir le formulaire
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

        # Zone vide au démarrage - les données s'afficheront après chargement/scraping
        if 'df' not in st.session_state and 'show_feedback' not in st.session_state:
            pass  # Rien à afficher, juste le header en haut

        # Gestion du scraping
        if scraper_btn:
            st.markdown("""
            <div class="alert-info">
                <strong>🔍 Scraping en cours...</strong><br>
                Veuillez patienter pendant la collecte des données.
            </div>
            """, unsafe_allow_html=True)

            config = categories[categorie_selectionnee]
            df = scraper_categorie(
                categorie_selectionnee,
                config['url'],
                nb_pages,
                config['selector']
            )

            st.session_state['df'] = df
            st.session_state['categorie'] = categorie_selectionnee
            st.session_state['show_feedback'] = False

            st.markdown(f"""
            <div class="alert-success">
                <strong>✅ Scraping terminé avec succès!</strong><br>
                {len(df)} annonces collectées et nettoyées
            </div>
            """, unsafe_allow_html=True)

        # Affichage des résultats quand des données sont disponibles (mais pas si feedback est affiché)
        if 'df' in st.session_state and not st.session_state.get('show_feedback', False):
            df = st.session_state['df']
            categorie = st.session_state['categorie']

            # Header avec le nom de la catégorie
            st.markdown(f"""
            <div class="section-header">
                <h2>📊 Analyse : {categorie}</h2>
            </div>
            """, unsafe_allow_html=True)

            # KPIs - Indicateurs clés
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📊 TOTAL ANNONCES", len(df))

            with col2:
                image_count = df['image_link'].notna().sum() if 'image_link' in df.columns else 0
                st.metric("🖼️ AVEC IMAGE", image_count)

            with col3:
                completion = round((df.notna().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
                st.metric("✅ COMPLÉTUDE", f"{completion}%")

            st.markdown("<br><br>", unsafe_allow_html=True)

            # Tabs pour organiser le contenu
            tab1, tab2, tab3 = st.tabs(["📊 Visualisations", "📋 Tableau de données", "💾 Export"])

            with tab1:
                st.markdown("### Analyse Graphique")
                fig = visualiser_donnees(df, categorie)
                st.pyplot(fig)

                # Informations supplémentaires
                st.markdown("---")
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    if 'price' in df.columns:
                        df_temp = df.copy()
                        df_temp['price_num'] = df_temp['price'].str.extract(r'(\d+)').astype(float)
                        prices_valid = df_temp['price_num'].dropna()
                        if len(prices_valid) > 0:
                            st.metric("Prix moyen", f"{prices_valid.mean():,.0f} CFA")
                with col_info2:
                    if 'address' in df.columns:
                        nb_villes = df['address'].nunique()
                        st.metric("Nombre de villes", nb_villes)

            with tab2:
                st.markdown("### Données brutes")

                st.dataframe(df, use_container_width=True, height=450)
                st.caption(f"Affichage de {len(df)} annonces")

            with tab3:
                st.markdown("### Téléchargement des données")

                st.info("💡 Exportez vos données pour des analyses plus approfondies dans Excel, Google Sheets, ou tout autre outil d'analyse.")

                col1, col2 = st.columns(2)

                with col1:
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Télécharger CSV",
                        data=csv,
                        file_name=f"{categorie.replace(' ', '_')}_data.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                with col2:
                    excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
                    df.to_excel(excel_buffer, index=False)
                    excel_buffer.close()

                    with open('temp.xlsx', 'rb') as f:
                        st.download_button(
                            label="📥 Télécharger Excel",
                            data=f,
                            file_name=f"{categorie.replace(' ', '_')}_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

