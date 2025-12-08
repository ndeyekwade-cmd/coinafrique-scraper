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

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a1f2e;
            border-right: 1px solid rgba(0,131,184,0.2);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }

        /* Bouton pour ouvrir/fermer le sidebar */
        [data-testid="collapsedControl"] {
            display: block;
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
            background-color: #f0f0f0;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            color: var(--text-dark);
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-red) 100%);
            color: white;
        }

        /* DataFrame */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            border: 1px solid rgba(0,131,184,0.2);
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
        df['price_num'] = df['price'].str.extract(r'(\d+)').astype(float)
        prices_valid = df['price_num'].dropna()

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
    with st.sidebar:
        st.markdown("## 📊 MENU")
        st.markdown("---")

        # Données pré-collectées
        with st.expander("📂 Données pré-collectées", expanded=True):
            st.markdown("**Charger des données existantes**")

            datasets_disponibles = {
                "Chiens (860 annonces)": "chiens.csv",
                "Moutons (1324 annonces)": "moutons.csv",
                "Lapins/Poules/Pigeons (804 annonces)": "lapins_poules_pigeons.csv",
                "Autres Animaux (491 annonces)": "autres_animaux.csv"
            }

            dataset_choisi = st.selectbox(
                "Sélectionner un jeu de données:",
                list(datasets_disponibles.keys()),
                key="dataset_select"
            )

            if st.button("CHARGER LES DONNÉES", use_container_width=True, key="load_data_btn"):
                try:
                    fichier = datasets_disponibles[dataset_choisi]
                    df = pd.read_csv(fichier, encoding='utf-8-sig')

                    # Renommer les colonnes pour correspondre au format attendu
                    if 'adress' in df.columns:
                        df = df.rename(columns={'adress': 'address', 'img_link': 'image_link'})

                    # Garder seulement les colonnes nécessaires
                    colonnes_necessaires = ['name', 'price', 'address', 'image_link']
                    df = df[[col for col in colonnes_necessaires if col in df.columns]]

                    st.session_state['df'] = df
                    st.session_state['categorie'] = dataset_choisi.split(' (')[0]
                    st.success(f"✅ {len(df)} annonces chargées!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors du chargement: {str(e)}")

        with st.expander("📈 Visualiser les données", expanded=False):
            if 'df' in st.session_state:
                st.success(f"✅ {len(st.session_state['df'])} annonces disponibles")
                if st.button("Voir les statistiques", key="view_stats"):
                    st.session_state['show_section'] = 'stats'
            else:
                st.info("Aucune donnée disponible. Chargez des données existantes ou lancez un scraping.")

        with st.expander("🔍 Scraper de nouvelles données", expanded=False):
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
                "📋 Catégorie:",
                list(categories.keys()),
                key="cat_select"
            )

            nb_pages = st.number_input(
                "📄 Nombre de pages:",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
                key="nb_pages_input"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            scraper_btn = st.button("🚀 LANCER", use_container_width=True, key="scrape_btn")

        with st.expander("💬 Feedback", expanded=False):
            st.markdown("**Votre avis compte!**")
            feedback = st.text_area(
                "Partagez vos commentaires:",
                placeholder="Que pensez-vous de cette application?",
                height=100,
                key="feedback_text"
            )
            if st.button("📤 Envoyer", use_container_width=True, key="send_feedback"):
                if feedback:
                    st.success("Merci pour votre feedback!")
                else:
                    st.warning("Veuillez écrire un commentaire.")

        st.markdown("---")
        st.markdown("**AIMS Senegal**")
        st.caption("© 2025 Ndeye Khady Wade")

    # ========== ZONE PRINCIPALE DU DASHBOARD ==========

    # Si aucune donnée n'est chargée, afficher la page d'accueil du dashboard
    if 'df' not in st.session_state:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <h1 style="color: #0083B8; font-size: 3rem; text-align: center; margin-bottom: 1rem;">
            Bienvenue sur votre Dashboard
        </h1>
        <p style="color: #e8e8e8; font-size: 1.3rem; text-align: center; margin-bottom: 1rem;">
            Utilisez le menu à gauche pour commencer
        </p>
        <p style="color: #F71938; font-size: 1rem; text-align: center; margin-bottom: 3rem;">
            ← Si le menu n'est pas visible, cliquez sur la flèche en haut à gauche
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Utiliser des colonnes Streamlit pour les cartes
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            col_card1, col_card2 = st.columns(2)

            with col_card1:
                st.markdown("""
                <div style="background: rgba(26, 31, 46, 0.8); border: 1px solid rgba(0,131,184,0.3);
                            border-radius: 12px; padding: 2rem; height: 200px;">
                    <h3 style="color: #0083B8; margin-top: 0;">📂 Option 1</h3>
                    <p style="color: #e8e8e8; line-height: 1.6;">
                        <strong>Charger des données existantes</strong><br><br>
                        Accédez instantanément à 3479 annonces déjà collectées
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col_card2:
                st.markdown("""
                <div style="background: rgba(26, 31, 46, 0.8); border: 1px solid rgba(247,25,56,0.3);
                            border-radius: 12px; padding: 2rem; height: 200px;">
                    <h3 style="color: #F71938; margin-top: 0;">🔍 Option 2</h3>
                    <p style="color: #e8e8e8; line-height: 1.6;">
                        <strong>Scraper de nouvelles données</strong><br><br>
                        Collectez des données fraîches en temps réel
                    </p>
                </div>
                """, unsafe_allow_html=True)

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

        st.markdown(f"""
        <div class="alert-success">
            <strong>✅ Scraping terminé avec succès!</strong><br>
            {len(df)} annonces collectées et nettoyées
        </div>
        """, unsafe_allow_html=True)

    # Affichage des résultats quand des données sont disponibles
    if 'df' in st.session_state:
        df = st.session_state['df']
        categorie = st.session_state['categorie']

        # Header avec le nom de la catégorie
        st.markdown(f"""
        <div class="section-header">
            <h2>📊 Analyse : {categorie}</h2>
        </div>
        """, unsafe_allow_html=True)

        # KPIs - Indicateurs clés
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("📊 TOTAL ANNONCES", len(df))

        with col2:
            st.metric("💰 AVEC PRIX", df['price'].notna().sum())

        with col3:
            st.metric("📍 AVEC ADRESSE", df['address'].notna().sum())

        with col4:
            st.metric("🖼️ AVEC IMAGE", df['image_link'].notna().sum())

        with col5:
            completion = round((df.notna().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
            st.metric("COMPLÉTUDE", f"{completion}%")

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

            # Options de filtrage
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                if st.checkbox("Afficher uniquement avec prix"):
                    df_display = df[df['price'].notna()]
                else:
                    df_display = df
            with col_filter2:
                if st.checkbox("Afficher uniquement avec adresse"):
                    df_display = df_display[df_display['address'].notna()]

            st.dataframe(df_display, use_container_width=True, height=450)
            st.caption(f"Affichage de {len(df_display)} sur {len(df)} annonces")

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
