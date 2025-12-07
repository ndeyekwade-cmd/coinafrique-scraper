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

# CSS Dashboard professionnel
st.markdown("""
<style>
    /* Variables de couleurs */
    :root {
        --aims-red: #8B1538;
        --aims-red-dark: #6B0F2A;
        --bg-light: #f8f9fa;
        --text-dark: #2d3436;
        --border-color: #dee2e6;
    }

    /* Background général */
    .stApp {
        background-color: var(--bg-light);
    }

    /* Barre latérale */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--border-color);
    }

    /* En-tête Dashboard */
    .dashboard-header {
        background: linear-gradient(135deg, var(--aims-red) 0%, var(--aims-red-dark) 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .dashboard-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .dashboard-subtitle {
        font-size: 0.95rem;
        margin-top: 0.3rem;
        opacity: 0.95;
    }

    /* Cartes de statistiques */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 3px solid var(--aims-red);
        transition: transform 0.2s;
        height: 100%;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--aims-red);
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .metric-icon {
        font-size: 2rem;
        opacity: 0.2;
        float: right;
    }

    /* Boutons */
    .stButton>button {
        background: var(--aims-red);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(139,21,56,0.2);
    }

    .stButton>button:hover {
        background: var(--aims-red-dark);
        box-shadow: 0 4px 8px rgba(139,21,56,0.3);
        transform: translateY(-1px);
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: var(--aims-red);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: var(--aims-red);
        color: white;
    }

    /* Alert boxes */
    .alert-box {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }

    .alert-success {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }

    .alert-info {
        background: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }

    .alert-warning {
        background: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }

    /* Section containers */
    .section-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--bg-light);
    }

    /* Footer */
    .dashboard-footer {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
        border-top: 3px solid var(--aims-red);
    }

    /* Sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Selectbox & Input */
    .stSelectbox, .stNumberInput {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête du Dashboard
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">📊 CoinAfrique Analytics Dashboard</h1>
    <p class="dashboard-subtitle">Plateforme d'analyse et de collecte de données | AIMS Senegal</p>
</div>
""", unsafe_allow_html=True)

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
    fig.suptitle(f'ANALYSE DES DONNÉES - {categorie_name}', fontsize=16, fontweight='bold')

    # Top 10 des adresses
    if 'address' in df.columns and df['address'].notna().sum() > 0:
        top_addresses = df['address'].value_counts().head(10)
        axes[0].barh(range(len(top_addresses)), top_addresses.values, color='#3B82F6')
        axes[0].set_yticks(range(len(top_addresses)))
        axes[0].set_yticklabels(top_addresses.index, fontsize=9)
        axes[0].set_xlabel('Nombre d\'annonces')
        axes[0].set_title('Top 10 des adresses')
        axes[0].invert_yaxis()
        axes[0].grid(axis='x', alpha=0.3)

    # Distribution des prix
    if 'price' in df.columns:
        df['price_num'] = df['price'].str.extract(r'(\d+)').astype(float)
        prices_valid = df['price_num'].dropna()

        if len(prices_valid) > 0:
            axes[1].hist(prices_valid, bins=20, color='#10B981', edgecolor='black', alpha=0.7)
            axes[1].set_xlabel('Prix (CFA)')
            axes[1].set_ylabel('Fréquence')
            axes[1].set_title('Distribution des prix')
            axes[1].grid(axis='y', alpha=0.3)

            mean_price = prices_valid.mean()
            median_price = prices_valid.median()
            axes[1].axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_price:,.0f} CFA')
            axes[1].axvline(median_price, color='orange', linestyle='--', linewidth=2, label=f'Médiane: {median_price:,.0f} CFA')
            axes[1].legend()

    plt.tight_layout()
    return fig

# Sidebar pour la configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration du Scraping")
    st.markdown("---")
    st.markdown("**Sélectionnez les paramètres:**")

    categories = {
        "🐕 Chiens": {
            "url": "https://sn.coinafrique.com/categorie/chiens",
            "selector": "card-content",
            "color": "#3B82F6"
        },
        "🐑 Moutons": {
            "url": "https://sn.coinafrique.com/categorie/moutons",
            "selector": "description",
            "color": "#10B981"
        },
        "🐔 Poules, Lapins et Pigeons": {
            "url": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
            "selector": "description",
            "color": "#F59E0B"
        },
        "🐾 Autres Animaux": {
            "url": "https://sn.coinafrique.com/categorie/autres-animaux",
            "selector": "description",
            "color": "#EF4444"
        }
    }

    categorie_selectionnee = st.selectbox(
        "Choisir une catégorie:",
        list(categories.keys())
    )

    nb_pages = st.number_input(
        "Nombre de pages à scraper:",
        min_value=1,
        max_value=50,
        value=5,
        step=1
    )

    st.markdown("---")

    scraper_btn = st.button("🚀 Lancer le scraping", use_container_width=True)

# Corps principal
if scraper_btn:
    st.markdown(f"""
    <div class="alert-box alert-info">
        <strong>🔍 Scraping en cours...</strong><br>
        Catégorie: {categorie_selectionnee}<br>
        Pages à scraper: {nb_pages}
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
    <div class="alert-box alert-success">
        <strong>✅ Scraping terminé avec succès!</strong><br>
        {len(df)} annonces collectées et nettoyées
    </div>
    """, unsafe_allow_html=True)

# Affichage des résultats
if 'df' in st.session_state:
    df = st.session_state['df']
    categorie = st.session_state['categorie']

    # Section: Statistiques KPIs
    st.markdown("## 📈 Indicateurs Clés de Performance")

    # Statistiques en cartes
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📊</span>
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">Total Annonces</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">💰</span>
            <div class="metric-value">{df['price'].notna().sum()}</div>
            <div class="metric-label">Avec Prix</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📍</span>
            <div class="metric-value">{df['address'].notna().sum()}</div>
            <div class="metric-label">Avec Adresse</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">🖼️</span>
            <div class="metric-value">{df['image_link'].notna().sum()}</div>
            <div class="metric-label">Avec Image</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Onglets pour les différentes vues
    st.markdown("## 📊 Analyse des Données")
    tab1, tab2, tab3 = st.tabs(["📊 Visualisations", "📋 Tableau de Données", "💾 Exporter"])

    with tab1:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        fig = visualiser_donnees(df, categorie)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown(f"**Catégorie:** {categorie} | **Nombre total:** {len(df)} annonces")
        st.dataframe(df, use_container_width=True, height=450)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("### 💾 Options d'Export")

        col1, col2 = st.columns(2)

        with col1:
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger en CSV",
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
                    label="📥 Télécharger en Excel",
                    data=f,
                    file_name=f"{categorie.replace(' ', '_')}_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Message d'accueil avec style dashboard
    st.markdown("""
    <div class="alert-box alert-info">
        <strong>👋 Bienvenue sur le Dashboard CoinAfrique!</strong><br>
        Configurez vos paramètres dans la barre latérale et lancez le scraping pour commencer l'analyse.
    </div>
    """, unsafe_allow_html=True)

    # Vue d'ensemble
    st.markdown("## 🎯 Vue d'Ensemble")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-container">
            <h3 class="section-title">📊 Fonctionnalités</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="padding: 0.5rem 0;">✅ Scraping automatisé de 4 catégories</li>
                <li style="padding: 0.5rem 0;">✅ Nettoyage intelligent des données</li>
                <li style="padding: 0.5rem 0;">✅ Visualisations analytiques avancées</li>
                <li style="padding: 0.5rem 0;">✅ Export multi-format (CSV, Excel)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-container">
            <h3 class="section-title">📈 Catégories Disponibles</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="padding: 0.5rem 0;">🐕 Chiens</li>
                <li style="padding: 0.5rem 0;">🐑 Moutons</li>
                <li style="padding: 0.5rem 0;">🐔 Poules, Lapins et Pigeons</li>
                <li style="padding: 0.5rem 0;">🐾 Autres Animaux</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer Dashboard
st.markdown("---")
st.markdown("""
<div class="dashboard-footer">
    <div style="margin-bottom: 0.5rem;">
        <strong style="font-size: 1.1rem;">📊 CoinAfrique Analytics Dashboard</strong>
    </div>
    <div style="color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;">
        AIMS Senegal | African Institute for Mathematical Sciences
    </div>
    <div style="color: #adb5bd; font-size: 0.85rem; margin-top: 0.5rem;">
        © 2025 Projet Data Collection | Ndeye Khady Wade
    </div>
</div>
""", unsafe_allow_html=True)
