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

        /* Sidebar fixe */
        [data-testid="stSidebar"] {
            background-color: #1a1f2e;
            border-right: 1px solid rgba(0,131,184,0.2);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }

        /* Masquer le bouton de collapse sidebar */
        [data-testid="collapsedControl"] {
            display: none;
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
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: var(--text-light);
            border: 1px solid rgba(0,131,184,0.3);
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

        /* Text general */
        p, span, label, div {
            color: var(--text-light);
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Fonction de scraping
@st.cache_data
def scraper_categorie(categorie_name, url, max_pages, selector_name):
    """Scrape une catégorie d'animaux"""
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
        # Pour Streamlit Cloud avec chromium
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

    # Nettoyage
    df = df.dropna(how='all')
    df = df.drop_duplicates(subset=['name', 'price', 'address'], keep='first')

    return df

# Fonction de visualisation
def visualiser_donnees(df, categorie_name):
    """Créer des visualisations pour une catégorie"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'ANALYSE DES DONNÉES - {categorie_name}', fontsize=16, fontweight='bold', color='#070505')

    # Top 10 des adresses
    if 'address' in df.columns and df['address'].notna().sum() > 0:
        top_addresses = df['address'].value_counts().head(10)
        axes[0].barh(range(len(top_addresses)), top_addresses.values, color='#0083B8')
        axes[0].set_yticks(range(len(top_addresses)))
        axes[0].set_yticklabels(top_addresses.index, fontsize=9)
        axes[0].set_xlabel('Nombre d\'annonces', fontweight='bold')
        axes[0].set_title('Top 10 des adresses', fontweight='bold')
        axes[0].invert_yaxis()
        axes[0].grid(axis='x', alpha=0.3, color='#cecdcd')

    # Distribution des prix
    if 'price' in df.columns:
        df['price_num'] = df['price'].str.extract(r'(\d+)').astype(float)
        prices_valid = df['price_num'].dropna()

        if len(prices_valid) > 0:
            axes[1].hist(prices_valid, bins=20, color='#F71938', edgecolor='black', alpha=0.7)
            axes[1].set_xlabel('Prix (CFA)', fontweight='bold')
            axes[1].set_ylabel('Fréquence', fontweight='bold')
            axes[1].set_title('Distribution des prix', fontweight='bold')
            axes[1].grid(axis='y', alpha=0.3, color='#cecdcd')

            mean_price = prices_valid.mean()
            median_price = prices_valid.median()
            axes[1].axvline(mean_price, color='#0083B8', linestyle='--', linewidth=2, label=f'Moyenne: {mean_price:,.0f} CFA')
            axes[1].axvline(median_price, color='orange', linestyle='--', linewidth=2, label=f'Médiane: {median_price:,.0f} CFA')
            axes[1].legend()

    plt.tight_layout()
    return fig

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ CONFIGURATION")
    st.markdown("---")

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
        "📋 Choisir une catégorie:",
        list(categories.keys())
    )

    nb_pages = st.number_input(
        "📄 Nombre de pages à scraper:",
        min_value=1,
        max_value=50,
        value=5,
        step=1
    )

    st.markdown("---")

    scraper_btn = st.button("🚀 LANCER LE SCRAPING", use_container_width=True)

# ==================== HEADER ====================
st.markdown("""
<div class="section-header">
    <h2>📊 CoinAfrique Analytics Dashboard</h2>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
if scraper_btn:
    st.markdown("""
    <div class="alert-info">
        <strong>🔍 Scraping en cours...</strong><br>
        Veuillez patienter pendant la collecte des données.
    </div>
    """, unsafe_allow_html=True)

    # Scraping
    config = categories[categorie_selectionnee]
    df = scraper_categorie(
        categorie_selectionnee,
        config['url'],
        nb_pages,
        config['selector']
    )

    # Stocker dans session state
    st.session_state['df'] = df
    st.session_state['categorie'] = categorie_selectionnee

    st.markdown(f"""
    <div class="alert-success">
        <strong>✅ Scraping terminé avec succès!</strong><br>
        {len(df)} annonces collectées et nettoyées
    </div>
    """, unsafe_allow_html=True)

# Affichage des résultats
if 'df' in st.session_state:
    df = st.session_state['df']
    categorie = st.session_state['categorie']

    # KPIs en 5 colonnes
    st.markdown("### 📈 INDICATEURS CLÉS")
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
        st.metric("✅ COMPLÉTUDE", f"{completion}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 VISUALISATIONS", "📋 DONNÉES", "💾 EXPORT"])

    with tab1:
        st.markdown("### 📊 Analyse Graphique")
        fig = visualiser_donnees(df, categorie)
        st.pyplot(fig)

    with tab2:
        st.markdown(f"### 📋 Tableau des Données - {categorie}")
        st.dataframe(df, use_container_width=True, height=450)

    with tab3:
        st.markdown("### 💾 Télécharger les Données")

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

else:
    # Page d'accueil
    st.markdown("""
    <div class="alert-info">
        <strong>👋 Bienvenue sur le Dashboard CoinAfrique!</strong><br><br>
        <b>Instructions:</b><br>
        1️⃣ Sélectionnez une catégorie d'animaux dans la barre latérale<br>
        2️⃣ Choisissez le nombre de pages à scraper (1-50)<br>
        3️⃣ Cliquez sur "LANCER LE SCRAPING" pour démarrer<br>
        4️⃣ Visualisez et exportez vos données
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Catégories Disponibles")
        st.markdown("""
        - 🐕 **Chiens**
        - 🐑 **Moutons**
        - 🐔 **Poules, Lapins et Pigeons**
        - 🐾 **Autres Animaux**
        """)

    with col2:
        st.markdown("### ✨ Fonctionnalités")
        st.markdown("""
        - ✅ Scraping automatisé
        - ✅ Nettoyage des données
        - ✅ Visualisations interactives
        - ✅ Export CSV & Excel
        """)

# Footer
st.markdown("""
<div class="custom-footer">
    <strong>📊 CoinAfrique Analytics Dashboard</strong><br>
    AIMS Senegal - Projet Data Collection | Ndeye Khady Wade<br>
    © 2025 African Institute for Mathematical Sciences
</div>
""", unsafe_allow_html=True)
