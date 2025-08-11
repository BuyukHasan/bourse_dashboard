from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.dashboard import Dashboard
from src.portfolio_manager import PortfolioManager
from src.reddit_analyzer import RedditSentiment
from src.news_fetcher import NewsFetcher
import random
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

def set_global_theme(theme_name):
    """Définit le thème global et stocke les couleurs dans session_state"""
    themes = {
        "Neon Cyberpunk": {
            "primary": "#0f0c29",
            "secondary": "#ff00ff",
            "background": "#100e1d",
            "accent1": "#00ffff",
            "accent2": "#ff00ff",
            "text": "#e0e0ff"
        },
        "Lava Explosion": {
            "primary": "#2a0000",
            "secondary": "#ff3c00",
            "background": "#1a0000",
            "accent1": "#ff7b00",
            "accent2": "#ff0000",
            "text": "#ffd9d9"
        },
        "Electric Ocean": {
            "primary": "#001f3f",
            "secondary": "#00ffff",
            "background": "#001a33",
            "accent1": "#0074D9",
            "accent2": "#7FDBFF",
            "text": "#aaffff"
        },
        "Acid Jungle": {
            "primary": "#001100",
            "secondary": "#00cc00",
            "background": "#000800",
            "accent1": "#00aa00",
            "accent2": "#008800",
            "text": "#e0ffe0"
        },
        "Galactic Purple": {
            "primary": "#0d000d",
            "secondary": "#cc00ff",
            "background": "#080008",
            "accent1": "#9900ff",
            "accent2": "#ff00cc",
            "text": "#f0e0ff"
        }
    }
    st.session_state.theme = theme_name
    st.session_state.theme_colors = themes.get(theme_name, themes["Neon Cyberpunk"])

def apply_global_theme():
    """Applique le thème visuel global à toute l'application"""
    colors = st.session_state.get('theme_colors', {
        'primary': '#0f0c29',
        'secondary': '#ff00ff',
        'background': '#100e1d',
        'accent1': '#00ffff',
        'accent2': '#ff00ff',
        'text': '#e0e0ff'
    })
    
    st.markdown(f"""
    <style>
        /* Fond principal et conteneurs */
        .stApp, .main, .block-container {{
            background-color: {colors['background']} !important;
            color: {colors['text']} !important;
        }}
    
        /* Texte général */
        p, div, h1, h2, h3, h4, h5, h6, span, label {{
            color: {colors['text']} !important;
        }}
    
        /* Inputs et sélecteurs */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select,
        .stTextArea>div>div>textarea {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border-color: {colors['secondary']} !important;
        }}
    
        /* Métriques et indicateurs */
        .stMetric {{
            border-left: 0.4rem solid {colors['secondary']};
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: {colors['primary']};
            color: {colors['text']};
            box-shadow: 0 0 15px {colors['accent1']};
        }}
    
        /* Onglets */
        .stTabs {{
            margin-bottom: 1rem;
        }}
        
        .stTabs [role="tablist"] {{
            gap: 0.5rem;
            padding: 0.25rem;
            background: transparent;
        }}
        
        .stTabs button[role="tab"] {{
            all: unset;
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border-radius: 0.5rem 0.5rem 0 0 !important;
            border: 1px solid {colors['secondary']} !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease !important;
            font-weight: normal !important;
            margin: 0 !important;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .stTabs button[role="tab"]:not([aria-selected="true"]):hover {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
            transform: translateY(-2px);
        }}
        
        .stTabs button[aria-selected="true"] {{
            background-color: {colors['secondary']} !important;
            color: {colors['primary']} !important;
            font-weight: bold !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            border-bottom: 3px solid {colors['accent1']} !important;
        }}
        
        .stTabs button[aria-selected="true"]::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 3px;
            background: {colors['accent1']};
            animation: tabUnderline 0.3s ease-out;
        }}
        
        .stTabs [role="tabpanel"] {{
            padding: 1.5rem !important;
            background: {colors['primary']} !important;
            border-radius: 0 0.5rem 0.5rem 0.5rem !important;
            border: 1px solid {colors['secondary']} !important;
            margin-top: -1px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }}
        
        @keyframes tabUnderline {{
            from {{ transform: scaleX(0); }}
            to {{ transform: scaleX(1); }}
        }}
    
        /* En-tête */
        .css-1vq4p4l {{
            padding: 2rem 1rem;
            background-color: {colors['primary']};
            color: {colors['text']};
            border-bottom: 2px solid {colors['accent1']};
        }}
    
        /* Alertes */
        .stAlert {{
            background-color: {colors['primary']};
            border: 1px solid {colors['secondary']};
            color: {colors['text']};
        }}
    
        /* Boutons */
        .stButton>button {{
            background-color: {colors['primary']};
            color: {colors['text']};
            border: 1px solid {colors['secondary']};
            border-radius: 0.5rem;
            transition: all 0.3s;
        }}
        .stButton>button:hover {{
            background-color: {colors['secondary']};
            color: {colors['primary']};
            box-shadow: 0 0 15px {colors['accent2']};
        }}
    
        /* DataFrames */
        .stDataFrame {{
            border: 1px solid {colors['secondary']};
            border-radius: 0.5rem;
            background-color: {colors['primary']} !important;
        }}
    
        /* Graphiques Plotly */
        .js-plotly-plot .plotly {{
            background-color: {colors['primary']} !important;
        }}
    
        /* Barre latérale */
        [data-testid="stSidebar"] {{
            background-color: {colors['primary']} !important;
        }}
    
        /* Contraste amélioré pour les thèmes problématiques */
        .stMarkdown strong, .stMarkdown b {{
            color: {colors['accent1']} !important;
        }}
        
        /* Écran de chargement */
        .loading-screen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: {colors['background']};
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            opacity: 1;
            transition: opacity 0.5s ease;
        }}
        
        .loading-content {{
            text-align: center;
            max-width: 400px;
            padding: 2rem;
            border-radius: 15px;
            background: rgba(15, 12, 41, 0.85);
            box-shadow: 0 0 30px {colors['accent1']}, 
                        0 0 50px rgba(0, 255, 255, 0.3);
        }}
        
        .loading-logo {{
            width: 180px;
            height: 180px;
            position: relative;
            margin: 0 auto 20px;
            animation: pulse 2.5s infinite ease-in-out;
        }}
        
        .logo-circle {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 3px solid transparent;
            border-top-color: {colors['accent1']};
            animation: spin 1.5s linear infinite;
        }}
        
        .logo-circle:nth-child(2) {{
            border-top-color: {colors['accent2']};
            animation-delay: -0.5s;
            width: 160px;
            height: 160px;
            top: 10px;
            left: 10px;
        }}
        
        .logo-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {colors['accent1']};
            font-weight: bold;
            font-size: 1.4rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px {colors['accent1']},
                         0 0 20px {colors['accent1']};
            animation: text-pulse 1.5s infinite alternate;
        }}
        
        .loading-text {{
            color: {colors['accent1']};
            font-size: 1.6rem;
            margin-top: 10px;
            font-family: 'Arial', sans-serif;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 8px rgba(0, 255, 255, 0.7);
            animation: glow 2s infinite alternate;
        }}
        
        .loading-subtext {{
            color: {colors['text']};
            font-size: 1rem;
            margin-top: 15px;
            opacity: 0.8;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(0.95); opacity: 0.9; }}
            50% {{ transform: scale(1.05); opacity: 1; }}
            100% {{ transform: scale(0.95); opacity: 0.9; }}
        }}
        
        @keyframes glow {{
            0% {{ text-shadow: 0 0 5px {colors['accent1']}; opacity: 0.8; }}
            100% {{ text-shadow: 0 0 20px {colors['accent1']}, 0 0 30px {colors['accent1']}; opacity: 1; }}
        }}
        
        @keyframes text-pulse {{
            0% {{ opacity: 0.7; transform: translate(-50%, -50%) scale(0.95); }}
            100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.05); }}
        }}
        
        /* ===== CORRECTIONS AJOUTÉES POUR LES ÉLÉMENTS D'INTERFACE ===== */
        /* Barre latérale - Titres */
        .css-1vq4p4l h1, 
        .css-1vq4p4l h2, 
        .css-1vq4p4l h3, 
        .css-1vq4p4l h4, 
        .css-1vq4p4l h5, 
        .css-1vq4p4l h6 {{
            color: {colors['accent1']} !important;
        }}
        
        /* Barre latérale - Texte général */
        .css-1vq4p4l, 
        .css-1vq4p4l p, 
        .css-1vq4p4l div, 
        .css-1vq4p4l span, 
        .css-1vq4p4l label {{
            color: {colors['text']} !important;
        }}
        
        /* Sélecteurs (Selectbox) */
        .stSelectbox > label {{
            color: {colors['text']} !important;
            font-weight: bold;
        }}
        
        .stSelectbox > div > div > select {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        .stSelectbox > div > div > div > svg {{
            fill: {colors['accent1']} !important;
        }}
        
        /* Date pickers */
        .stDateInput > label {{
            color: {colors['text']} !important;
            font-weight: bold;
        }}
        
        .stDateInput > div > div > input {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        .stDateInput > div > div > button {{
            color: {colors['accent1']} !important;
        }}
        
        /* Multiselect */
        .stMultiSelect > label {{
            color: {colors['text']} !important;
            font-weight: bold;
        }}
        
        .stMultiSelect > div > div > div {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        .stMultiSelect span[data-baseweb="tag"] {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
        }}
        
        /* Boutons */
        .stButton > button {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
            font-weight: bold;
        }}
        
        .stButton > button:hover {{
            background-color: {colors['secondary']} !important;
            color: {colors['primary']} !important;
            box-shadow: 0 0 15px {colors['accent2']} !important;
        }}
        
        /* Alertes */
        .stAlert {{
            background-color: {colors['primary']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        .stAlert h3 {{
            color: {colors['accent1']} !important;
        }}
        
        .stAlert p {{
            color: {colors['text']} !important;
        }}
        
        /* Zone de texte */
        .stTextArea > label {{
            color: {colors['text']} !important;
            font-weight: bold;
        }}
        
        .stTextArea > div > div > textarea {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        /* Barre de progression */
        .stProgress > div > div > div {{
            background-color: {colors['accent1']} !important;
        }}
        
        /* Spinner */
        .stSpinner > div > div {{
            border-color: {colors['accent1']} !important;
            border-right-color: transparent !important;
        }}
        
        /* Placeholder texte */
        ::placeholder {{
            color: {colors['accent2']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Tooltips */
        .stTooltip {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}
        
        /* Contenu des tooltips */
        .stTooltip p {{
            color: {colors['text']} !important;
        }}
        
        /* Sélecteur de thème */
        .stRadio > label {{
            color: {colors['text']} !important;
            font-weight: bold;
        }}
        
        .stRadio [role="radiogroup"] {{
            background-color: {colors['primary']} !important;
            border: 1px solid {colors['secondary']} !important;
            padding: 10px;
            border-radius: 8px;
        }}
        
        .stRadio [role="radio"] {{
            color: {colors['text']} !important;
        }}
        
        .stRadio [role="radio"][aria-checked="true"] {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
            font-weight: bold;
        }}
        
        /* ===== CORRECTIONS SPÉCIFIQUES POUR LES SÉLECTEURS ===== */
        /* Cible tous les widgets de sélection */
        div[data-baseweb="select"] > div:first-child {{
            background-color: {colors['primary']} !important;
            border-color: {colors['secondary']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Texte dans les sélecteurs */
        div[data-baseweb="select"] div {{
            color: {colors['text']} !important;
        }}
        
        /* Icônes des sélecteurs */
        div[data-baseweb="select"] svg {{
            fill: {colors['accent1']} !important;
        }}
        
        /* Options du menu déroulant */
        div[data-baseweb="popover"] div {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Options au survol */
        div[data-baseweb="popover"] li:hover {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
        }}
        
        /* Sélecteur de mode dans la sidebar */
        .stSidebar div[data-baseweb="select"] {{
            background-color: {colors['background']} !important;
        }}
        
        /* Multiselect - éléments sélectionnés */
        span[data-baseweb="tag"] {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
        }}
        
        /* Date picker - calendrier */
        .rdrMonth {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Boutons du date picker */
        .rdrDayToday span:after {{
            background-color: {colors['accent1']} !important;
        }}
        
        /* Inputs de date */
        input[data-baseweb="input"] {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border-color: {colors['secondary']} !important;
        }}
        
        /* Forcer la couleur du texte dans tous les widgets */
        .st-bb, .st-at, .st-ae, .st-af, .st-ag, .stSelectbox label, .stDateInput label, .stMultiSelect label {{
            color: {colors['text']} !important;
        }}
        
        /* Conteneur principal de la sidebar */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {colors['primary']} !important;
        }}
    </style>
    """
    , unsafe_allow_html=True)
def test_dashboard(df):
    """Full test of Dashboard class"""
    print("\n" + "="*50)
    print("DASHBOARD TEST".center(50))
    print("="*50)
    
    try:
        print("\n[1] Initializing Dashboard...")
        dashboard = Dashboard(df)
        print("✅ Dashboard initialized successfully")
        
        print("\n[2] Testing full display...")
        placeholder = st.empty()
        with placeholder.container():
            dashboard.display()
        
        print("✅ Dashboard displayed without duplicates")
        print("\n✅ All Dashboard tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard error: {str(e)}")
        return False

def test_visualizer(df):
    """Full test of Visualizer class"""
    print("\n" + "="*50)
    print("VISUALIZER TEST".center(50))
    print("="*50)
    
    try:
        print("\n[1] 2x2: MA_draw + Rsi_draw(show_zones=True)")
        viz1 = Visualizer(df, rows=2, columns=2, row_heights=[0.6, 0.4])
        viz1.MA_draw().Rsi_draw(show_zones=True).show()

        print("\n[2] 2x2: candlestick + MA_draw(overlay=True) + RSI")
        viz2 = Visualizer(df, rows=2, columns=2, row_heights=[0.6, 0.4])
        viz2.draw_candlestick() \
            .MA_draw(overlay=True) \
            .Rsi_draw(show_zones=True) \
            .show()

        print("\n[3] 3x1: candlestick, volume, cumulative returns")
        viz3 = Visualizer(df, rows=3, columns=1, row_heights=[0.5, 0.25, 0.25])
        viz3.draw_candlestick() \
            .draw_volume() \
            .draw_cumulative_returns() \
            .show()

        print("\n[4] 1x1: all plots as overlay")
        viz4 = Visualizer(df, rows=1, columns=1)
        viz4.draw_candlestick(overlay=True) \
            .MA_draw(overlay=True) \
            .Rsi_draw(show_zones=True, overlay=True) \
            .draw_volume(overlay=True) \
            .draw_cumulative_returns(overlay=True) \
            .show()

        print("\n[5] 2x2 with reset_position() between two plots")
        viz5 = Visualizer(df, rows=2, columns=2)
        viz5.MA_draw()
        viz5.reset_position()
        viz5.Rsi_draw(show_zones=False)
        viz5.show()

        print("\n✅ All Visualizer tests passed")
        return True

    except Exception as e:
        print(f"❌ Visualizer error: {e}")
        return False

def test_data_fetcher():
    """Full test of DataFetcher with error handling"""
    print("\n" + "="*50)
    print("DATA_FETCHER TEST".center(50))
    print("="*50)
    
    try:
        print("\n[1] Initialization...")
        fetcher = DataFetcher("TSLA")
        print(f"✅ Success - Ticker: {fetcher.ticker}")
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        return False

    tests = [
        {"name": "6-month data", "params": {"period": "6mo"}, "min_rows": 120},
        {"name": "1-month data", "params": {"period": "1mo"}, "min_rows": 20},
        {"name": "Specific date range", "params": {"start": "2025-07-01", "end": "2025-07-15"}, "min_rows": 10}
    ]

    for test in tests:
        print(f"\n[2] Test: {test['name']}...")
        try:
            df = fetcher.fetch_data(**test['params'])
            if df.empty:
                print(f"❌ No data returned ({test['name']})")
                return False
            print(f"✅ Retrieved {len(df)} rows")
            print(f"Columns: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    print("\n[3] Real-time data test...")
    try:
        realtime = fetcher.real_time_data()
        if not realtime.empty:
            print("✅ Latest quote:")
            print(realtime[['Open', 'High', 'Low', 'Close']])
        else:
            print("⚠️ No real-time data (market closed?)")
    except Exception as e:
        print(f"❌ Real-time data error: {str(e)}")
        return False

    return True

def test_technical_analyzer(df):
    """Full test of TechnicalAnalyzer class"""
    print("\n" + "="*50)
    print("TECHNICAL_ANALYZER TEST".center(50))
    print("="*50)
    
    try:
        analyzer = TechnicalAnalyzer(df)
        print("✅ Initialization successful")
    except Exception as e:
        print(f"❌ Initialization error: {str(e)}")
        return False

    tests = [
        {"name": "50/200-day Moving Averages", "func": analyzer.compute_50_200_days, "check_cols": ['MA_50', 'MA_200']},
        {"name": "RSI Indicator", "func": lambda: analyzer.add_rsi(14), "check_cols": ['rsi']},
        {"name": "Trading Signals", "func": analyzer.add_signal_column, "check_cols": ['Signal']},
        {"name": "Daily Performance", "func": analyzer.add_performance_column, "check_cols": ['Daily_Return']},
        {"name": "Bollinger Bands", "func": lambda: analyzer.bollinger_bands(window=20), "check_cols": ['MA_BB', 'Upper_Band', 'Lower_Band']},
        {"name": "Return Calculation", "func": analyzer.add_returns_columns, "check_cols": ['returns']}
    ]

    for test in tests:
        print(f"\n➡️ Test: {test['name']}")
        try:
            test['func']()
            missing = [col for col in test['check_cols'] if col not in analyzer.df.columns]
            if missing:
                print(f"❌ Missing columns: {missing}")
            else:
                print(f"✅ Success - Columns added: {test['check_cols']}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print("\n📊 Final data summary:")
    print(analyzer.df.tail(3)[['Close', 'MA_50', 'MA_200', 'rsi', 'Signal', 'Daily_Return']])
    
    return True

def test_multi_asset_comparison():
    """Multi-asset comparison test"""
    print("\n" + "="*50)
    print("MULTI-ASSET COMPARISON TEST".center(50))
    print("="*50)
    
    try:
        print("\n[1] Fetching data for 3 assets...")
        tickers = ["AAPL", "MSFT", "GOOGL"]
        data = {}
        
        for t in tickers:
            df = DataFetcher(t).fetch_data(period="6mo")
            analyzer = TechnicalAnalyzer(df)
            analyzer.compute_50_200_days()
            data[t] = analyzer.df
            print(f"✅ {t}: {len(df)} days retrieved")
        
        print("\n[2] Creating comparison chart...")
        viz = Visualizer(data["AAPL"], rows=1, columns=1)
        
        print("\n[3] Displaying comparison curves")
        viz.draw_multiple_tickers({
            "Apple": data["AAPL"],
            "Microsoft": data["MSFT"],
            "Google": data["GOOGL"]
        })
        
        viz.fig.update_layout(
            title="Performance Comparison",
            yaxis_title="Closing Price ($)",
            hovermode="x unified"
        )
        
        st.plotly_chart(viz.fig, use_container_width=True)
        print("\n✅ Multi-asset comparison test successful")
        return True
        
    except Exception as e:
        print(f"❌ Comparison error: {str(e)}")
        return False

def portfolio_mode():
    st.title("🎯 Virtual Portfolio")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_tickers = st.multiselect(
            "Select assets", 
            ["AAPL", "TSLA", "MSFT", "GOOGL"],
            default=["AAPL", "MSFT"]
        )
    with col2:
        weights = []
        for ticker in selected_tickers:
            weight = st.number_input(
                f"Weight of {ticker} (%)", 
                min_value=0, max_value=100, value=50
            )
            weights.append(weight / 100)
    
    if sum(weights) != 1.0:
        st.error("Sum of weights must equal 100%!")
        return
    
    tickers_weights = dict(zip(selected_tickers, weights))
    
    if st.button("Run simulation"):
        pm = PortfolioManager(tickers_weights)
        pm.fetch_portfolio_data(period="6mo")
        returns = pm.calculate_weighted_returns()
        metrics = pm.get_performance_metrics()
        
        fig = Visualizer(returns, rows=1, columns=1)
        fig._add_trace(
            go.Scatter(
                x=returns.index,
                y=returns['Cumulative_Return'],
                name="Portfolio Performance",
                line=dict(color="royalblue", width=3)
            ),
            row=1, col=1
        )
        st.plotly_chart(fig.fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Annualized Return", f"{metrics['annualized_return']:.2f}%")
        col2.metric("Volatility", f"{metrics['volatility']:.2f}%")
        col3.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")

def test_news_fetcher():
    """NewsFetcher test with simulation"""
    print("\n" + "="*50)
    print("NEWS FETCHER TEST".center(50))
    print("="*50)
    
    try:
        fetcher = NewsFetcher()
        news = fetcher.get_company_news("AAPL")
        
        if not news:
            print("❌ No news retrieved")
            return False
        
        print(f"✅ {len(news)} articles retrieved")
        for i, item in enumerate(news[:3]):
            print(f"{i+1}. {item['title']} ({item['sentiment']})")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_reddit_sentiment():
    """RedditSentiment test with simulation"""
    print("\n" + "="*50)
    print("REDDIT SENTIMENT TEST".center(50))
    print("="*50)
    
    try:
        analyzer = RedditSentiment()
        data = analyzer.analyze_ticker("TSLA")
        
        print(f"✅ Results: Positive={data['positive']}, Neutral={data['neutral']}, Negative={data['negative']}")
        print(f"Total: {data['total']}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_portfolio_manager():
    """PortfolioManager test"""
    print("\n" + "="*50)
    print("PORTFOLIO MANAGER TEST".center(50))
    print("="*50)
    
    try:
        tickers_weights = {"AAPL": 0.6, "MSFT": 0.4}
        pm = PortfolioManager(tickers_weights)
        
        dates = pd.date_range(end=datetime.today(), periods=100, freq='D')
        data = {}
        for ticker in tickers_weights:
            df = pd.DataFrame({
                'Close': [random.uniform(100, 200) for _ in range(100)],
                'Daily_Return': [random.uniform(-0.05, 0.05) for _ in range(100)]
            }, index=dates)
            data[ticker] = df
        
        pm.data = data
        returns = pm.calculate_weighted_returns()
        
        if 'Portfolio_Return' not in returns.columns:
            print("❌ Missing Portfolio_Return column")
            return False
        
        metrics = pm.get_performance_metrics()
        print(f"✅ Annualized return: {metrics['annualized_return']:.2f}%")
        print(f"✅ Volatility: {metrics['volatility']:.2f}%")
        print(f"✅ Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_alert_system():
    """Alert system test"""
    print("\n" + "="*50)
    print("ALERT SYSTEM TEST".center(50))
    print("="*50)
    
    try:
        dates = pd.date_range(end=datetime.today(), periods=10, freq='D')
        df = pd.DataFrame({
            'Close': [150, 152, 155, 153, 156, 158, 160, 159, 162, 165],
            'rsi': [30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
            'Volatility': [0.01, 0.02, 0.015, 0.018, 0.02, 0.022, 0.025, 0.03, 0.028, 0.026],
            'MA_50': [150, 151, 152, 153, 154, 155, 156, 157, 158, 159],
            'MA_200': [145, 146, 147, 148, 149, 150, 151, 152, 153, 154]
        }, index=dates)
        
        dashboard = Dashboard(df)
        
        st.session_state.alerts = [
            {'indicator': 'RSI', 'condition': 'Above', 'threshold': 70, 'active': True, 'triggered': False},
            {'indicator': 'Closing Price', 'condition': 'Above', 'threshold': 160, 'active': True, 'triggered': False},
            {'indicator': 'MA Crossover', 'condition': 'Crosses above', 'threshold': 0, 'active': True, 'triggered': False}
        ]
        
        dashboard._check_alerts()
        
        alerts_triggered = [a['triggered'] for a in st.session_state.alerts]
        if all(alerts_triggered):
            print("✅ All alerts triggered")
            return True
        else:
            print(f"❌ Alerts not triggered: {alerts_triggered}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

@st.cache_data(ttl=3600, show_spinner=False)
def load_initial_data():
    fetcher = DataFetcher("AAPL")
    df = fetcher.fetch_data(period="6mo")
    analyzer = TechnicalAnalyzer(df)
    analyzer.compute_50_200_days()
    analyzer.add_rsi()
    analyzer.calculate_volatility()
    return analyzer.df

@st.cache_data(ttl=3600, show_spinner=False)
def load_comparison_data(tickers, start_date, end_date):
    compare_data = {}
    for t in tickers:
        df = DataFetcher(t).fetch_data(start=start_date, end=end_date)
        if not df.empty:
            analyzer = TechnicalAnalyzer(df)
            analyzer.compute_50_200_days()
            compare_data[t] = analyzer.df
    return compare_data

def main():
    st.set_page_config(page_title="Stock Market Dashboard", layout="wide")
    
    # Initialiser le thème par défaut si nécessaire
    if 'theme' not in st.session_state:
        set_global_theme("Neon Cyberpunk")
    
    # Ajouter le sélecteur de thème dans la sidebar
    with st.sidebar:
        st.title("Configuration")
        
        # Sélecteur de mode
        mode = st.selectbox(
            "Select mode",
            [
                "Single Stock Dashboard", 
                "Multi-Asset Comparison", 
                "Virtual Portfolio",
                "Unit Tests"
            ],
            key="mode_selector_unique"
        )
        
        # Nouveau sélecteur de thème
        st.subheader("Theme Settings")
        theme_names = ["Neon Cyberpunk", "Lava Explosion", "Electric Ocean", "Acid Jungle", "Galactic Purple"]
        current_theme = st.session_state.get('theme', "Neon Cyberpunk")
        selected_theme = st.selectbox(
            "Choose a theme",
            theme_names,
            index=theme_names.index(current_theme),
            key="theme_selector"
        )

        # Mettre à jour le thème si changement
        if selected_theme != st.session_state.theme:
            set_global_theme(selected_theme)
    
    # Appliquer le thème global (doit être après la mise à jour du thème)
    apply_global_theme()
    
    # Afficher l'écran de chargement avec le thème actuel
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        colors = st.session_state.get('theme_colors', {
            'primary': '#0f0c29',
            'secondary': '#ff00ff',
            'background': '#100e1d',
            'accent1': '#00ffff',
            'accent2': '#ff00ff',
            'text': '#e0e0ff'
        })
        
        st.markdown(f"""
        <div class="loading-screen">
            <div class="loading-content">
                <div class="loading-logo">
                    <div class="logo-circle"></div>
                    <div class="logo-circle"></div>
                    <div class="logo-text">HB's<br>PRODUCTION</div>
                </div>
                <div class="loading-text">MARKET ANALYZER</div>
                <div class="loading-subtext">Chargement des données financières...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    start_time = time.time()
    min_loading_time = 2.0

    # Le reste du code main...
    if mode == "Single Stock Dashboard":
        if 'df' not in st.session_state:
            fetcher = DataFetcher("AAPL")
            df = fetcher.fetch_data(period="6mo")
            analyzer = TechnicalAnalyzer(df)
            analyzer.compute_50_200_days()
            analyzer.add_rsi()
            analyzer.calculate_volatility()
            analyzer.add_signal_column()
            analyzer.add_performance_column()
            analyzer.add_returns_columns()
            st.session_state.df = analyzer.df
        
        dashboard = Dashboard(st.session_state.df)
        dashboard.display()
    
    elif mode == "Multi-Asset Comparison":
        st.title("Multi-Asset Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            tickers = st.multiselect(
                "Select stocks to compare",
                ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL"],
                default=["AAPL", "MSFT", "GOOGL"],
                key="comparison_tickers"
            )
        with col2:
            start_date = st.date_input("Start date", value=datetime.now().replace(year=datetime.now().year-1))
            end_date = st.date_input("End date", value=datetime.now())
        
        if st.button("Run comparison", key="run_comparison"):
            compare_data = {}
            progress_bar = st.progress(0)
            
            for i, t in enumerate(tickers):
                try:
                    df = DataFetcher(t).fetch_data(start=start_date, end=end_date)
                    if not df.empty:
                        analyzer = TechnicalAnalyzer(df)
                        analyzer.compute_50_200_days()
                        analyzer.add_rsi()
                        analyzer.calculate_volatility()
                        analyzer.add_signal_column()
                        analyzer.add_performance_column()
                        analyzer.add_returns_columns()
                        compare_data[t] = analyzer.df
                    else:
                        st.warning(f"No data available for {t}")
                except Exception as e:
                    st.error(f"Error with {t}: {str(e)}")
                progress_bar.progress((i+1) / len(tickers))
            
            if compare_data:
                st.session_state.compare_data = compare_data
        
        if "compare_data" in st.session_state and st.session_state.compare_data:
            viz = Visualizer(next(iter(st.session_state.compare_data.values())), rows=1, columns=1)
            viz.draw_multiple_tickers(st.session_state.compare_data)
            
            viz.fig.update_layout(
                title="Performance Comparison",
                yaxis_title="Closing Price ($)",
                hovermode="x unified",
                height=600
            )
            
            st.plotly_chart(viz.fig, use_container_width=True)
    
    elif mode == "Virtual Portfolio":
        portfolio_mode()
    
    elif mode == "Unit Tests":
        st.title("🧪 Unit Tests")
        
        tests = {
            "DataFetcher": test_data_fetcher,
            "TechnicalAnalyzer": lambda: test_technical_analyzer(st.session_state.df if 'df' in st.session_state else None),
            "Visualizer": lambda: test_visualizer(st.session_state.df if 'df' in st.session_state else None),
            "Multi-Asset Comparison": test_multi_asset_comparison,
            "NewsFetcher": test_news_fetcher,
            "RedditSentiment": test_reddit_sentiment,
            "PortfolioManager": test_portfolio_manager,
            "Alert System": test_alert_system
        }
        
        selected_test = st.selectbox("Select a test to run", list(tests.keys()), key="test_selector")
        
        if st.button("Run test", key="run_test"):
            with st.spinner("Running..."):
                try:
                    success = tests[selected_test]()
                    if success:
                        st.success("✅ Test successful!")
                    else:
                        st.error("❌ Test failed")
                except Exception as e:
                    st.error(f"❌ Test error: {str(e)}")
            
            st.text_area("Logs", value="See console for details", height=100, key="logs_area")
    elapsed = time.time() - start_time
    if elapsed < min_loading_time:
        time.sleep(min_loading_time - elapsed)
    loading_placeholder.empty()
main()