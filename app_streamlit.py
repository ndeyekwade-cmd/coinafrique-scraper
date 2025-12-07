import streamlit as st
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import time

# Configuration de la page
st.set_page_config(
    page_title="CoinAfrique Scraper",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS simple avec couleur AIMS
st.markdown("""
<style>
    /* En-tête simple */
    .header-container {
        background: #8B1538;
        padding: 2rem;
        border-radius: 0.8rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }

    .header-subtitle {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }

    /* Cartes simples */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8B1538;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #8B1538;
    }

    .stat-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* Bouton simple */
    .stButton>button {
        background: #8B1538;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: 600;
    }

    .stButton>button:hover {
        background: #6B0F2A;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #8B1538;
    }

    /* Tabs */
    .stTabs [aria-selected="true"] {
        background-color: #8B1538 !important;
        color: white;
    }

    /* Boxes */
    .success-box {
        background: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    .info-box {
        background: #FEF3C7;
        border-left: 4px solid #8B1538;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    /* Footer */
    .footer-aims {
        text-align: center;
        padding: 2rem;
        background: #8B1538;
        color: white;
        border-radius: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête de l'application avec logo AIMS
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("WhatsApp Image 2025-11-29 à 12.52.58_0067bc42.jpg", use_container_width=True)

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🐾 CoinAfrique Animal Scraper</h1>
    <p class="header-subtitle">Scraping intelligent des annonces d'animaux sur CoinAfrique.com</p>
    <div class="aims-badge">
        AIMS SENEGAL | African Institute for Mathematical Sciences
    </div>
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
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

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
    <div class="info-box">
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
    <div class="success-box">
        <strong>✅ Scraping terminé!</strong><br>
        {len(df)} annonces collectées et nettoyées
    </div>
    """, unsafe_allow_html=True)

# Affichage des résultats
if 'df' in st.session_state:
    df = st.session_state['df']
    categorie = st.session_state['categorie']

    # Statistiques en cartes
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(df)}</div>
            <div class="stat-label">Total Annonces</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{df['price'].notna().sum()}</div>
            <div class="stat-label">Avec Prix</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{df['address'].notna().sum()}</div>
            <div class="stat-label">Avec Adresse</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{df['image_link'].notna().sum()}</div>
            <div class="stat-label">Avec Image</div>
        </div>
        """, unsafe_allow_html=True)

    # Onglets pour les différentes vues
    tab1, tab2, tab3 = st.tabs(["📊 Visualisations", "📋 Données", "💾 Export"])

    with tab1:
        st.markdown("### 📊 Analyse visuelle des données")
        fig = visualiser_donnees(df, categorie)
        st.pyplot(fig)

    with tab2:
        st.markdown("### 📋 Tableau des données")
        st.dataframe(df, use_container_width=True, height=400)

    with tab3:
        st.markdown("### 💾 Exporter les données")

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
    # Message d'accueil
    st.markdown("""
    <div class="info-box">
        <strong>👋 Bienvenue!</strong><br>
        Sélectionnez une catégorie dans la barre latérale et cliquez sur "Lancer le scraping" pour commencer.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🎯 Fonctionnalités")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - ✅ Scraping de 4 catégories d'animaux
        - ✅ Nettoyage automatique des données
        - ✅ Visualisations interactives
        """)

    with col2:
        st.markdown("""
        - ✅ Export CSV et Excel
        - ✅ Interface moderne et intuitive
        - ✅ Suivi en temps réel du scraping
        """)

# Footer AIMS
st.markdown("---")
st.markdown("""
<div class="footer-aims">
    <h3 style="margin: 0 0 1rem 0;">🐾 CoinAfrique Animal Scraper</h3>
    <p style="margin: 0.5rem 0; font-size: 1.1rem;">
        <strong>Développé avec ❤️ par AIMS Senegal</strong>
    </p>
    <p style="margin: 0.5rem 0; color: #D4AF37; font-size: 0.9rem;">
        African Institute for Mathematical Sciences | Centre d'Excellence en Sciences Mathématiques
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.85rem; opacity: 0.8;">
        © 2025 AIMS Senegal - Projet Data Collection | Ndeye Khady Wade
    </p>
</div>
""", unsafe_allow_html=True)
