import streamlit as st
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import time

# Page configuration
st.set_page_config(
    page_title="CoinAfrique Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# Load custom CSS
def local_css():
    st.markdown("""
    <style>
        /* Color variables */
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

        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Night blue background */
        .stApp {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        }

        /* Main content - offset for sidebar */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }

        /* Sidebar - Force visibility */
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

        /* Button to open/close sidebar */
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

        /* Metric containers with colored shadows */
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

        /* Buttons */
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

        /* Pointer cursor for selectbox */
        div[data-baseweb="select"],
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] > div,
        div[data-testid="stSelectbox"] > div > div {
            cursor: pointer !important;
        }

        /* Pointer cursor for dropdown menu options */
        div[role="listbox"],
        div[role="option"] {
            cursor: pointer !important;
        }

        /* Titles */
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

        /* Welcome animations */
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

# Scraping function
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

# Visualization function
def visualiser_donnees(df, categorie_name):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'DATA ANALYSIS - {categorie_name}', fontsize=16, fontweight='bold', color='#e8e8e8')
    fig.patch.set_facecolor('#1a1f2e')

    if 'address' in df.columns and df['address'].notna().sum() > 0:
        top_addresses = df['address'].value_counts().head(10)
        axes[0].barh(range(len(top_addresses)), top_addresses.values, color='#0083B8')
        axes[0].set_yticks(range(len(top_addresses)))
        axes[0].set_yticklabels(top_addresses.index, fontsize=9, color='#e8e8e8')
        axes[0].set_xlabel('Number of ads', fontweight='bold', color='#e8e8e8')
        axes[0].set_title('Top 10 addresses', fontweight='bold', color='#e8e8e8')
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
            axes[1].set_xlabel('Price (CFA)', fontweight='bold', color='#e8e8e8')
            axes[1].set_ylabel('Frequency', fontweight='bold', color='#e8e8e8')
            axes[1].set_title('Price distribution', fontweight='bold', color='#e8e8e8')
            axes[1].grid(axis='y', alpha=0.3, color='#cecdcd')
            axes[1].set_facecolor('#1a1f2e')
            axes[1].tick_params(colors='#e8e8e8')

            mean_price = prices_valid.mean()
            median_price = prices_valid.median()
            axes[1].axvline(mean_price, color='#0083B8', linestyle='--', linewidth=2, label=f'Mean: {mean_price:,.0f} CFA')
            axes[1].axvline(median_price, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_price:,.0f} CFA')
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
        <p class="welcome-subtitle">Data analysis and collection platform</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-btn-wrapper">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("→ VISIT", key="welcome_btn"):
            st.session_state.page = 'instructions'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE INSTRUCTIONS ====================
elif st.session_state.page == 'instructions':
    st.markdown("""
    <div class="section-header">
        <h2>User Guide</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="instructions-container">', unsafe_allow_html=True)

    # Introduction
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Welcome to CoinAfrique Analytics</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                This platform allows you to automatically collect and analyze data
                from animal ads posted on CoinAfrique Senegal. The tool extracts key information
                (name, price, location, images) and generates visualizations to facilitate your analysis.
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <strong style="color: #F71938;">Two options are available:</strong><br>
                <span style="color: #0083B8;">•</span> Load pre-collected data (3479 ads available)<br>
                <span style="color: #0083B8;">•</span> Scrape new data in real-time
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Option 1 - Pre-collected data
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Option 1: Load pre-collected data</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                <strong>Immediate access to 3479 already collected ads</strong>
            </p>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li><strong>Dogs:</strong> 860 ads</li>
                <li><strong>Sheep:</strong> 1324 ads</li>
                <li><strong>Rabbits/Chickens/Pigeons:</strong> 804 ads</li>
                <li><strong>Other Animals:</strong> 491 ads</li>
            </ul>
            <p style="margin-top: 1rem; line-height: 1.6;">
                In the sidebar, "Data" section, select the desired category
                and click "LOAD". The visualizations will appear
                instantly without waiting.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Option 2 - Scrape new data
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Option 2: Scrape new data</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                <strong>Collect fresh data in real-time</strong>
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">1</span>
                <strong>Choose a category:</strong> Select from Dogs, Sheep,
                Chickens/Rabbits/Pigeons, or Other Animals in the "Scraper" menu.
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">2</span>
                <strong>Define volume:</strong> Specify the number of pages (1-50).
                Approximately 20 ads per page. 5 pages = ~100 ads, 20 pages = ~400 ads.
            </p>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <span class="instruction-number">3</span>
                <strong>Start scraping:</strong> Click "START". A progress bar
                will track the progress. Duration: a few minutes depending on volume.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Analysis and export
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #0083B8; margin-top: 0;">Analyze and export your data</h3>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                Once the data is loaded or scraped, you have access to:
            </p>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li><strong>Key metrics:</strong> Total ads, prices, addresses, images, completeness</li>
                <li><strong>Visualizations:</strong> Top 10 addresses, price distribution with mean/median</li>
                <li><strong>Data table:</strong> Detailed view of all ads</li>
                <li><strong>Export:</strong> Download in CSV or Excel format</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Usage tips
    st.markdown("""
        <div class="instruction-card">
            <h3 style="color: #F71938; margin-top: 0;">Usage Tips</h3>
            <ul style="margin-left: 20px; line-height: 1.8;">
                <li>Start with pre-collected data for quick discovery</li>
                <li>For scraping, start with 5-10 pages to test</li>
                <li>Scraped data is cached to avoid repeated collections</li>
                <li>Use the sidebar to switch between loading and scraping</li>
                <li>Charts can be saved via right-click</li>
                <li>Check the completeness indicator before exporting</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br><br>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("START", key="start_scraping_btn"):
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

        /* Reduce space at top of page */
        .main > div:first-child {
            padding-top: 1rem !important;
        }
    </style>

    <h1 class="dashboard-title">Welcome to your Dashboard</h1>
    <p class="dashboard-subtitle">Use the left menu to start</p>
    """, unsafe_allow_html=True)

    # Simple style for separation only
    st.markdown("""
    <style>
        /* Separation bar between columns */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
            border-right: 4px solid #0083B8 !important;
            padding-right: 1rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
            padding-left: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create 2 columns: menu on left (limited), content on right (wide)
    col_menu, col_content = st.columns([0.7, 3.3])

    with col_menu:
        # Global style for menu column
        st.markdown("""
        <style>
            /* Target specifically the first column of the dashboard */
            section[data-testid="stVerticalBlock"] > div:has(button[key="load_data_btn"]) {
                background: linear-gradient(135deg, rgba(10, 15, 20, 0.95) 0%, rgba(20, 25, 35, 0.95) 100%) !important;
                padding: 1.5rem !important;
                border-radius: 8px !important;
                min-height: 70vh !important;
            }

            /* Reduce ALL spaces in the left menu */

            /* Compact expanders */
            div[data-testid="stExpander"] {
                margin-bottom: 0.3rem !important;
                margin-top: 0 !important;
            }

            /* Very compact expander content */
            div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
                padding: 0.3rem 0.5rem !important;
            }

            /* ALL vertical elements in expanders - minimal gap */
            div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
            div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"],
            div[data-testid="stExpander"] .element-container {
                gap: 0 !important;
                margin: 0 !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Selectbox - no space */
            div[data-testid="stExpander"] div[data-testid="stSelectbox"],
            div[data-testid="stExpander"] div[data-baseweb="select"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Labels - no space */
            div[data-testid="stExpander"] label {
                margin: 0 !important;
                padding: 0 !important;
                padding-bottom: 0.2rem !important;
                font-size: 0.85rem !important;
            }

            /* Number input - no space */
            div[data-testid="stExpander"] div[data-testid="stNumberInput"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Text area - no space */
            div[data-testid="stExpander"] div[data-testid="stTextArea"] {
                margin: 0 !important;
                padding-bottom: 0 !important;
            }

            /* Buttons - no space above */
            div[data-testid="stExpander"] div[data-testid="stButton"],
            div[data-testid="stExpander"] button {
                margin-top: 0 !important;
                margin-bottom: 0.2rem !important;
                padding: 0.3rem 1rem !important;
            }

            /* Force elements to stick together */
            div[data-testid="stExpander"] .stSelectbox + div,
            div[data-testid="stExpander"] .stNumberInput + div,
            div[data-testid="stExpander"] .stTextArea + div {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }

            /* Remove spaces between widgets */
            div[data-testid="column"]:first-child [data-testid="stVerticalBlock"] {
                gap: 0 !important;
            }

            div[data-testid="column"]:first-child .element-container {
                margin-bottom: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Pre-collected data
        with st.expander("📂 Data", expanded=True):

            datasets_disponibles = {
                "Dogs (860 ads)": "chiens.csv",
                "Sheep (1324 ads)": "moutons.csv",
                "Rabbits/Chickens/Pigeons (804 ads)": "lapins_poules_pigeons.csv",
                "Other Animals (491 ads)": "autres_animaux.csv"
            }

            dataset_choisi = st.selectbox(
                "Category:",
                list(datasets_disponibles.keys()),
                key="dataset_select"
            )

            if st.button("LOAD", use_container_width=True, key="load_data_btn"):
                try:
                    fichier = datasets_disponibles[dataset_choisi]
                    df = pd.read_csv(fichier, encoding='utf-8-sig')

                    # Rename columns to have consistent names
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

                    # Keep ALL columns from CSV
                    st.session_state['df'] = df
                    st.session_state['categorie'] = dataset_choisi.split(' (')[0]
                    st.session_state['show_feedback'] = False
                    st.success(f"✅ {len(df)} ads loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Loading error: {str(e)}")

        with st.expander("🔍 Scraper", expanded=False):
            categories = {
                "🐕 Dogs": {
                    "url": "https://sn.coinafrique.com/categorie/chiens",
                    "selector": "card-content"
                },
                "🐑 Sheep": {
                    "url": "https://sn.coinafrique.com/categorie/moutons",
                    "selector": "description"
                },
                "🐔 Chickens, Rabbits and Pigeons": {
                    "url": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
                    "selector": "description"
                },
                "🐾 Other Animals": {
                    "url": "https://sn.coinafrique.com/categorie/autres-animaux",
                    "selector": "description"
                }
            }

            categorie_selectionnee = st.selectbox(
                "Category:",
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

            scraper_btn = st.button("START", use_container_width=True, key="scrape_btn")

        with st.expander("💬 Feedback", expanded=False):
            if st.button("CHOOSE", use_container_width=True, key="feedback_btn"):
                st.session_state['show_feedback'] = True
                st.rerun()

    # ========== MAIN DASHBOARD AREA (right column) ==========
    with col_content:
        # Global style for content column
        st.markdown("""
        <style>
            /* Target content area */
            div[data-testid="stVerticalBlock"] div[data-testid="column"]:last-child > div {
                background: linear-gradient(135deg, rgba(35, 40, 50, 0.5) 0%, rgba(30, 35, 45, 0.5) 100%) !important;
                padding: 1.5rem !important;
                border-radius: 8px !important;
                min-height: 70vh !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Display feedback cards
        if 'show_feedback' in st.session_state and st.session_state['show_feedback']:
            st.markdown("""
            <div class="section-header">
                <h2>💬 Give your feedback</h2>
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
                        Share your experience with our Google form
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
                            Open form
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
                        Answer our survey on KoboToolbox
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
                            Open form
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

        else:
            # Empty zone at startup - data will appear after loading/scraping
            if 'df' not in st.session_state:
                pass  # Nothing to display, just the header at the top

            # Scraping management
            if scraper_btn:
            st.markdown("""
            <div class="alert-info">
                <strong>🔍 Scraping in progress...</strong><br>
                Please wait while collecting data.
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
                <strong>✅ Scraping completed successfully!</strong><br>
                {len(df)} ads collected and cleaned
            </div>
            """, unsafe_allow_html=True)

        # Display results when data is available (but not if feedback is displayed)
        if 'df' in st.session_state and not st.session_state.get('show_feedback', False):
            df = st.session_state['df']
            categorie = st.session_state['categorie']

            # Header with category name
            st.markdown(f"""
            <div class="section-header">
                <h2>📊 Analysis: {categorie}</h2>
            </div>
            """, unsafe_allow_html=True)

            # KPIs - Key indicators
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📊 TOTAL ADS", len(df))

            with col2:
                image_count = df['image_link'].notna().sum() if 'image_link' in df.columns else 0
                st.metric("🖼️ WITH IMAGE", image_count)

            with col3:
                completion = round((df.notna().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
                st.metric("✅ COMPLETENESS", f"{completion}%")

            st.markdown("<br><br>", unsafe_allow_html=True)

            # Tabs to organize content
            tab1, tab2, tab3 = st.tabs(["📊 Visualizations", "📋 Data Table", "💾 Export"])

            with tab1:
                st.markdown("### Graphical Analysis")
                fig = visualiser_donnees(df, categorie)
                st.pyplot(fig)

                # Additional information
                st.markdown("---")
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    if 'price' in df.columns:
                        df_temp = df.copy()
                        df_temp['price_num'] = df_temp['price'].str.extract(r'(\d+)').astype(float)
                        prices_valid = df_temp['price_num'].dropna()
                        if len(prices_valid) > 0:
                            st.metric("Average price", f"{prices_valid.mean():,.0f} CFA")
                with col_info2:
                    if 'address' in df.columns:
                        nb_villes = df['address'].nunique()
                        st.metric("Number of cities", nb_villes)

            with tab2:
                st.markdown("### Raw Data")

                st.dataframe(df, use_container_width=True, height=450)
                st.caption(f"Displaying {len(df)} ads")

            with tab3:
                st.markdown("### Download Data")

                st.info("💡 Export your data for more in-depth analysis in Excel, Google Sheets, or any other analysis tool.")

                col1, col2 = st.columns(2)

                with col1:
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Download CSV",
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
                            label="📥 Download Excel",
                            data=f,
                            file_name=f"{categorie.replace(' ', '_')}_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

