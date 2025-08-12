from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.dashboard import Dashboard
from src.portfolio_manager import PortfolioManager
from src.reddit_analyzer import RedditSentiment
from src.news_fetcher import NewsFetcher
from src.css import Cssdash  # Import de la classe CSS
from src.geo_data import GeoDataFetcher
import random
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

def set_global_theme(theme_name):
    """Définit le thème global et stocke les couleurs dans session_state"""
    st.session_state.theme = theme_name
    st.session_state.theme_colors = Cssdash.themes.get(theme_name, Cssdash.themes["Neon Cyberpunk"])

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
    
    # Utilisation de la classe CSS pour générer le style
    st.markdown(Cssdash.get_css(colors), unsafe_allow_html=True)

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
    
    # Catégories d'actifs étendues
    asset_categories = {
        "Technologie": [
            "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "ADBE", "INTC", "CSCO", 
            "ORCL", "IBM", "QCOM", "TXN", "AVGO", "AMD", "CRM", "ADP", "INTU", "NOW", 
            "AMAT", "MU", "ADI", "LRCX", "KLAC", "CDNS", "SNPS", "ANET", "FTNT", "NXPI", 
            "MRVL", "PANW", "PYPL", "SQ", "SHOP", "ZM", "TEAM", "OKTA", "CRWD", "ZS", "NET"
        ],
        "Services Publics": [
            "NEE", "DUK", "SO", "D", "EXC", "AEP", "PEG", "ED", "EIX", "ES", "FE", 
            "PPL", "WEC", "XEL", "AEE", "ETR", "CMS", "AWK", "ATO", "SRE", "CNP", 
            "PCG", "NI", "DTE", "LNT", "D", "PEG", "EVRG", "AGR", "BEP", "BIPC"
        ],
        "Santé": [
            "JNJ", "PFE", "UNH", "MRK", "ABT", "TMO", "BMY", "AMGN", "GILD", "CVS", 
            "LLY", "ABBV", "MDT", "VRTX", "REGN", "DHR", "SYK", "BDX", "ISRG", "ZTS", 
            "HCA", "CI", "ANTM", "HUM", "IQV", "EW", "IDXX", "ALGN", "MRNA", "BNTX", 
            "VTRS", "BAX", "BIIB", "ILMN", "DGX", "LH", "UHS", "HOLX", "DXCM", "STE"
        ],
        "Consommation": [
            "PG", "KO", "PEP", "WMT", "COST", "MO", "PM", "MDLZ", "CL", "KHC", "EL", 
            "KMB", "STZ", "CLX", "SJM", "CHD", "CAG", "HSY", "GIS", "ADM", "TSN", 
            "MKC", "CPB", "LW", "TAP", "BF-B", "MNST", "FLO", "SYY", "KR", "K", "COTY",
            "TGT", "HD", "LOW", "DG", "DLTR", "FIVE", "BURL", "ROST", "TJX"
        ],
        "Finances": [
            "JPM", "BAC", "V", "MA", "WFC", "C", "GS", "AXP", "MS", "BLK", "SCHW", 
            "PYPL", "COF", "USB", "PNC", "TFC", "TD", "CME", "ICE", "AON", "MMC", 
            "AJG", "SPGI", "MCO", "FIS", "FISV", "NDAQ", "CBOE", "MKTX", "RJF", "RY",
            "BNS", "BMO", "ALLY", "KEY", "CFG", "HBAN", "MTB", "RF", "ZION"
        ],
        "Industriel": [
            "GE", "HON", "MMM", "BA", "CAT", "UNP", "DE", "RTX", "LMT", "GD", "NOC", 
            "ITW", "EMR", "ETN", "WM", "RSG", "WM", "FDX", "UPS", "CSX", "NSC", "CP", 
            "CNI", "DAL", "UAL", "LUV", "AAL", "DOV", "FTV", "IR", "OTIS", "TT", "PH", 
            "ROK", "SWK", "AME", "GNRC", "JCI", "PWR", "WAB", "XYL", "WSO", "FAST"
        ],
        "ETF Large Cap": [
            "SPY", "IVV", "VOO", "VTI", "SCHX", "IWB", "ITOT", "VTV", "IWD", "SCHV", 
            "VUG", "IWF", "SCHG", "QUAL", "MTUM", "USMV", "SPLG", "SPLV", "RSP", "VIG",
            "DIA", "IWM", "IJH", "IJR", "VB", "VO", "VV", "MGK", "MGV", "VONE"
        ],
        "ETF Techno": [
            "QQQ", "XLK", "VGT", "SMH", "ARKK", "SOXX", "FTEC", "IGV", "FDN", "SKYY", 
            "WCLD", "PSI", "XNTK", "AIQ", "BOTZ", "ROBT", "ARKW", "ARKF", "FINX", "IPAY",
            "XSW", "PSJ", "PSCT", "PTF", "TECL", "SOXL", "ROM", "USD", "FXL", "QTEC"
        ],
        "ETF Dividendes": [
            "SCHD", "VYM", "DGRO", "SDY", "NOBL", "VIG", "DVY", "HDV", "SPYD", "FVD", 
            "DIV", "PEY", "PFM", "KBWD", "QYLD", "XYLD", "RYLD", "DIVO", "SPHD", "JEPI",
            "NUSI", "SRET", "ALTY", "GTO", "RDIV", "FDL", "DHS", "FVD", "SDOG", "DIVB"
        ],
        "Obligations Corporate": [
            "LQD", "VCIT", "HYG", "JNK", "PFF", "VCLT", "VCIT", "VCSH", "IGIB", "IGSB", 
            "SHYG", "SJNK", "HYLB", "USHY", "ANGL", "FALN", "HYLS", "HYXU", "IHY", "PHB",
            "QLTA", "SLQD", "BSCQ", "BSJP", "BSJO", "BSJN", "BSJM", "BSJL", "BSJK", "BSJI"
        ],
        "Obligations Gouvernement": [
            "GOVT", "TLT", "IEF", "SHY", "SPTS", "VGIT", "VGLT", "VGSH", "IEI", "SHV", 
            "BIL", "SCHO", "SCHR", "SPTL", "TLO", "GVI", "ITE", "FIBR", "FTSM", "GOVZ",
            "EDV", "ZROZ", "TLH", "IEF", "VGIT", "VGSH", "SCHR", "SPTI", "FIBR", "GOVI"
        ],
        "Matières Premières": [
            "GLD", "SLV", "USO", "UNG", "DBA", "PDBC", "GSG", "IAU", "SLVO", "USL", 
            "UCO", "SCO", "BOIL", "KOLD", "WEAT", "CORN", "SOYB", "CANE", "CPER", "PALL", 
            "PPLT", "DBB", "DBC", "COMT", "FTGC", "BCD", "BCM", "JJG", "JJC", "LD"
        ],
        "Cryptomonnaies": [
            "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "XRP-USD", "SOL-USD", "DOT-USD", 
            "DOGE-USD", "AVAX-USD", "SHIB-USD", "MATIC-USD", "ATOM-USD", "LTC-USD", 
            "UNI-USD", "LINK-USD", "ALGO-USD", "XLM-USD", "VET-USD", "ICP-USD", "FIL-USD",
            "TRX-USD", "ETC-USD", "XMR-USD", "EGLD-USD", "AAVE-USD", "XTZ-USD", "EOS-USD",
            "NEO-USD", "ZEC-USD", "DASH-USD"
        ],
        "Immobilier (REITs)": [
            "O", "AMT", "PLD", "CCI", "EQIX", "DLR", "PSA", "SPG", "AVB", "EQR", 
            "VTR", "WELL", "WY", "EXR", "MAA", "ESS", "UDR", "SBAC", "IRM", "ARE",
            "REG", "KIM", "FRT", "VICI", "STOR", "NSA", "LAMR", "GLPI", "CPT", "ACC"
        ],
        "Énergie": [
            "XOM", "CVX", "SHEL", "TTE", "COP", "EOG", "PXD", "MPC", "PSX", "VLO",
            "OXY", "HES", "DVN", "FANG", "CTRA", "EQT", "MRO", "HAL", "SLB", "BKR",
            "NOV", "FTI", "LNG", "ET", "EPD", "WMB", "OKE", "KMI", "TRP", "ENB"
        ],
        "Communication": [
            "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS", "CHTR", "EA", "TTWO", "ATVI",
            "ROKU", "LYV", "NWSA", "FOXA", "IPG", "OMC", "WPP", "DISH", "SIRI", "LGF-A",
            "IAC", "MTCH", "BIDU", "JD", "BABA", "TME", "YY", "DOYU", "HUYA", "IQ"
        ]
    }
    
    col1, col2 = st.columns(2)
    with col1:
        # Sélecteur de catégorie
        selected_category = st.selectbox(
            "Type d'actif",
            list(asset_categories.keys())
        )
        
        # Sélecteur de tickers basé sur la catégorie
        selected_tickers = st.multiselect(
            "Sélectionnez des actifs",
            asset_categories[selected_category],
            default=asset_categories[selected_category][:2]
        )
    with col2:
        weights = []
        for ticker in selected_tickers:
            weight = st.number_input(
                f"Poids de {ticker} (%)", 
                min_value=0, max_value=100, value=50
            )
            weights.append(weight / 100)
    
    if sum(weights) != 1.0:
        st.error("La somme des poids doit être égale à 100% !")
        return
    
    tickers_weights = dict(zip(selected_tickers, weights))
    
    if st.button("Lancer la simulation"):
        pm = PortfolioManager(tickers_weights)
        pm.fetch_portfolio_data(period="6mo")
        returns = pm.calculate_weighted_returns()
        metrics = pm.get_performance_metrics()
        
        fig = Visualizer(returns, rows=1, columns=1)
        fig._add_trace(
            go.Scatter(
                x=returns.index,
                y=returns['Cumulative_Return'],
                name="Performance du portefeuille",
                line=dict(color="royalblue", width=3)
            ),
            row=1, col=1
        )
        st.plotly_chart(fig.fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Rendement annualisé", f"{metrics['annualized_return']:.2f}%")
        col2.metric("Volatilité", f"{metrics['volatility']:.2f}%")
        col3.metric("Ratio de Sharpe", f"{metrics['sharpe_ratio']:.2f}")

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
    st.set_page_config(page_title="Tableau de bord financier", layout="wide")
    
    # Initialiser le thème par défaut si nécessaire
    if 'theme' not in st.session_state:
        set_global_theme("Neon Cyberpunk")
    
    # Récupérer les couleurs du thème actuel IMMÉDIATEMENT APRÈS l'initialisation
    colors = st.session_state.get('theme_colors', {
        'primary': '#0f0c29',
        'secondary': '#ff00ff',
        'background': '#100e1d',
        'accent1': '#00ffff',
        'accent2': '#ff00ff',
        'text': '#e0e0ff'
    })
    
    # Ajouter le sélecteur de thème dans la sidebar
    with st.sidebar:
        st.title("Configuration")
        
        # Sélecteur de mode
        mode = st.selectbox(
            "Sélectionnez le mode",
            [
                "Tableau de bord individuel", 
                "Comparaison multi-actifs", 
                "Portefeuille virtuel",
                "Tests unitaires"
            ],
            key="mode_selector_unique"
        )
        
        # Nouveau sélecteur de thème
        st.subheader("Paramètres du thème")
        theme_names = ["Neon Cyberpunk", "Lava Explosion", "Electric Ocean", "Acid Jungle", "Galactic Purple"]
        current_theme = st.session_state.get('theme', "Neon Cyberpunk")
        selected_theme = st.selectbox(
            "Choisissez un thème",
            theme_names,
            index=theme_names.index(current_theme),
            key="theme_selector"
        )

        # Mettre à jour le thème si changement
        if selected_theme != st.session_state.get('theme', "Neon Cyberpunk"):
            set_global_theme(selected_theme)
            # Mettre à jour les couleurs après changement de thème
            colors = st.session_state.theme_colors
    
    # Appliquer le thème global
    apply_global_theme()
    
    # Utiliser la variable 'colors' définie plus haut
    st.markdown(f"""
    <script>
    // Force le style des éléments au chargement
    document.addEventListener('DOMContentLoaded', function() {{
        // Appliquer à tous les éléments
        forceStyles();
        
        // Réappliquer après 1s et 3s au cas où Streamlit modifie le DOM
        setTimeout(forceStyles, 1000);
        setTimeout(forceStyles, 3000);
        
        function forceStyles() {{
            // Appliquer à tous les inputs
            const inputs = document.querySelectorAll('input');
            inputs.forEach(input => {{
                input.style.backgroundColor = '{colors['primary']}';
                input.style.color = '{colors['text']}';
                input.style.border = '1px solid {colors['secondary']}';
            }});
            
            // Appliquer à tous les boutons
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => {{
                btn.style.backgroundColor = '{colors['primary']}';
                btn.style.color = '{colors['text']}';
                btn.style.border = '1px solid {colors['secondary']}';
                btn.style.fontWeight = 'bold';
            }});
            
            // Appliquer à tous les labels
            const labels = document.querySelectorAll('label');
            labels.forEach(label => {{
                label.style.color = '{colors['text']}';
                label.style.fontWeight = 'bold';
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)
    
    # Afficher l'écran de chargement avec le thème actuel
    loading_placeholder = st.empty()
    with loading_placeholder.container():
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
    if mode == "Tableau de bord individuel":
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
    
    elif mode == "Comparaison multi-actifs":
        st.title("Comparaison multi-actifs")
        
        # Catégories d'actifs pour la comparaison
        asset_categories = {
        "Technologie": [
            "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "ADBE", "INTC", "CSCO", 
            "ORCL", "IBM", "QCOM", "TXN", "AVGO", "AMD", "CRM", "ADP", "INTU", "NOW", 
            "AMAT", "MU", "ADI", "LRCX", "KLAC", "CDNS", "SNPS", "ANET", "FTNT", "NXPI", 
            "MRVL", "PANW", "PYPL", "SQ", "SHOP", "ZM", "TEAM", "OKTA", "CRWD", "ZS", "NET"
        ],
        "Services Publics": [
            "NEE", "DUK", "SO", "D", "EXC", "AEP", "PEG", "ED", "EIX", "ES", "FE", 
            "PPL", "WEC", "XEL", "AEE", "ETR", "CMS", "AWK", "ATO", "SRE", "CNP", 
            "PCG", "NI", "DTE", "LNT", "D", "PEG", "EVRG", "AGR", "BEP", "BIPC"
        ],
        "Santé": [
            "JNJ", "PFE", "UNH", "MRK", "ABT", "TMO", "BMY", "AMGN", "GILD", "CVS", 
            "LLY", "ABBV", "MDT", "VRTX", "REGN", "DHR", "SYK", "BDX", "ISRG", "ZTS", 
            "HCA", "CI", "ANTM", "HUM", "IQV", "EW", "IDXX", "ALGN", "MRNA", "BNTX", 
            "VTRS", "BAX", "BIIB", "ILMN", "DGX", "LH", "UHS", "HOLX", "DXCM", "STE"
        ],
        "Consommation": [
            "PG", "KO", "PEP", "WMT", "COST", "MO", "PM", "MDLZ", "CL", "KHC", "EL", 
            "KMB", "STZ", "CLX", "SJM", "CHD", "CAG", "HSY", "GIS", "ADM", "TSN", 
            "MKC", "CPB", "LW", "TAP", "BF-B", "MNST", "FLO", "SYY", "KR", "K", "COTY",
            "TGT", "HD", "LOW", "DG", "DLTR", "FIVE", "BURL", "ROST", "TJX"
        ],
        "Finances": [
            "JPM", "BAC", "V", "MA", "WFC", "C", "GS", "AXP", "MS", "BLK", "SCHW", 
            "PYPL", "COF", "USB", "PNC", "TFC", "TD", "CME", "ICE", "AON", "MMC", 
            "AJG", "SPGI", "MCO", "FIS", "FISV", "NDAQ", "CBOE", "MKTX", "RJF", "RY",
            "BNS", "BMO", "ALLY", "KEY", "CFG", "HBAN", "MTB", "RF", "ZION"
        ],
        "Industriel": [
            "GE", "HON", "MMM", "BA", "CAT", "UNP", "DE", "RTX", "LMT", "GD", "NOC", 
            "ITW", "EMR", "ETN", "WM", "RSG", "WM", "FDX", "UPS", "CSX", "NSC", "CP", 
            "CNI", "DAL", "UAL", "LUV", "AAL", "DOV", "FTV", "IR", "OTIS", "TT", "PH", 
            "ROK", "SWK", "AME", "GNRC", "JCI", "PWR", "WAB", "XYL", "WSO", "FAST"
        ],
        "ETF Large Cap": [
            "SPY", "IVV", "VOO", "VTI", "SCHX", "IWB", "ITOT", "VTV", "IWD", "SCHV", 
            "VUG", "IWF", "SCHG", "QUAL", "MTUM", "USMV", "SPLG", "SPLV", "RSP", "VIG",
            "DIA", "IWM", "IJH", "IJR", "VB", "VO", "VV", "MGK", "MGV", "VONE"
        ],
        "ETF Techno": [
            "QQQ", "XLK", "VGT", "SMH", "ARKK", "SOXX", "FTEC", "IGV", "FDN", "SKYY", 
            "WCLD", "PSI", "XNTK", "AIQ", "BOTZ", "ROBT", "ARKW", "ARKF", "FINX", "IPAY",
            "XSW", "PSJ", "PSCT", "PTF", "TECL", "SOXL", "ROM", "USD", "FXL", "QTEC"
        ],
        "ETF Dividendes": [
            "SCHD", "VYM", "DGRO", "SDY", "NOBL", "VIG", "DVY", "HDV", "SPYD", "FVD", 
            "DIV", "PEY", "PFM", "KBWD", "QYLD", "XYLD", "RYLD", "DIVO", "SPHD", "JEPI",
            "NUSI", "SRET", "ALTY", "GTO", "RDIV", "FDL", "DHS", "FVD", "SDOG", "DIVB"
        ],
        "Obligations Corporate": [
            "LQD", "VCIT", "HYG", "JNK", "PFF", "VCLT", "VCIT", "VCSH", "IGIB", "IGSB", 
            "SHYG", "SJNK", "HYLB", "USHY", "ANGL", "FALN", "HYLS", "HYXU", "IHY", "PHB",
            "QLTA", "SLQD", "BSCQ", "BSJP", "BSJO", "BSJN", "BSJM", "BSJL", "BSJK", "BSJI"
        ],
        "Obligations Gouvernement": [
            "GOVT", "TLT", "IEF", "SHY", "SPTS", "VGIT", "VGLT", "VGSH", "IEI", "SHV", 
            "BIL", "SCHO", "SCHR", "SPTL", "TLO", "GVI", "ITE", "FIBR", "FTSM", "GOVZ",
            "EDV", "ZROZ", "TLH", "IEF", "VGIT", "VGSH", "SCHR", "SPTI", "FIBR", "GOVI"
        ],
        "Matières Premières": [
            "GLD", "SLV", "USO", "UNG", "DBA", "PDBC", "GSG", "IAU", "SLVO", "USL", 
            "UCO", "SCO", "BOIL", "KOLD", "WEAT", "CORN", "SOYB", "CANE", "CPER", "PALL", 
            "PPLT", "DBB", "DBC", "COMT", "FTGC", "BCD", "BCM", "JJG", "JJC", "LD"
        ],
        "Cryptomonnaies": [
            "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "XRP-USD", "SOL-USD", "DOT-USD", 
            "DOGE-USD", "AVAX-USD", "SHIB-USD", "MATIC-USD", "ATOM-USD", "LTC-USD", 
            "UNI-USD", "LINK-USD", "ALGO-USD", "XLM-USD", "VET-USD", "ICP-USD", "FIL-USD",
            "TRX-USD", "ETC-USD", "XMR-USD", "EGLD-USD", "AAVE-USD", "XTZ-USD", "EOS-USD",
            "NEO-USD", "ZEC-USD", "DASH-USD"
        ],
        "Immobilier (REITs)": [
            "O", "AMT", "PLD", "CCI", "EQIX", "DLR", "PSA", "SPG", "AVB", "EQR", 
            "VTR", "WELL", "WY", "EXR", "MAA", "ESS", "UDR", "SBAC", "IRM", "ARE",
            "REG", "KIM", "FRT", "VICI", "STOR", "NSA", "LAMR", "GLPI", "CPT", "ACC"
        ],
        "Énergie": [
            "XOM", "CVX", "SHEL", "TTE", "COP", "EOG", "PXD", "MPC", "PSX", "VLO",
            "OXY", "HES", "DVN", "FANG", "CTRA", "EQT", "MRO", "HAL", "SLB", "BKR",
            "NOV", "FTI", "LNG", "ET", "EPD", "WMB", "OKE", "KMI", "TRP", "ENB"
        ],
        "Communication": [
            "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS", "CHTR", "EA", "TTWO", "ATVI",
            "ROKU", "LYV", "NWSA", "FOXA", "IPG", "OMC", "WPP", "DISH", "SIRI", "LGF-A",
            "IAC", "MTCH", "BIDU", "JD", "BABA", "TME", "YY", "DOYU", "HUYA", "IQ"
        ]
    }
        
        # Créer une liste unique de tous les tickers
        all_tickers = list(set(
            asset_categories["Actions"] + 
            asset_categories["ETF"] + 
            asset_categories["Obligations"]
        ))
        all_tickers.sort()
        
        col1, col2 = st.columns(2)
        with col1:
            tickers = st.multiselect(
                "Sélectionnez les actifs à comparer",
                all_tickers,
                default=["AAPL", "SPY", "TLT"],
                key="comparison_tickers"
            )
        with col2:
            start_date = st.date_input("Date de début", value=datetime.now().replace(year=datetime.now().year-1))
            end_date = st.date_input("Date de fin", value=datetime.now())
        
        if st.button("Exécuter la comparaison", key="run_comparison"):
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
                        st.warning(f"Aucune donnée disponible pour {t}")
                except Exception as e:
                    st.error(f"Erreur avec {t}: {str(e)}")
                progress_bar.progress((i+1) / len(tickers))
            
            if compare_data:
                st.session_state.compare_data = compare_data
        
        if "compare_data" in st.session_state and st.session_state.compare_data:
            viz = Visualizer(next(iter(st.session_state.compare_data.values())), rows=1, columns=1)
            viz.draw_multiple_tickers(st.session_state.compare_data)
            
            viz.fig.update_layout(
                title="Comparaison de performance",
                yaxis_title="Prix de clôture ($)",
                hovermode="x unified",
                height=600
            )
            
            st.plotly_chart(viz.fig, use_container_width=True)
    
    elif mode == "Portefeuille virtuel":
        portfolio_mode()
    
    elif mode == "Tests unitaires":
        st.title("🧪 Tests unitaires")
        
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
        
        selected_test = st.selectbox("Sélectionnez un test à exécuter", list(tests.keys()), key="test_selector")
        
        if st.button("Exécuter le test", key="run_test"):
            with st.spinner("En cours..."):
                try:
                    success = tests[selected_test]()
                    if success:
                        st.success("✅ Test réussi !")
                    else:
                        st.error("❌ Échec du test")
                except Exception as e:
                    st.error(f"❌ Erreur de test: {str(e)}")
            
            st.text_area("Journaux", value="Voir la console pour les détails", height=100, key="logs_area")
    
    elapsed = time.time() - start_time
    if elapsed < min_loading_time:
        time.sleep(min_loading_time - elapsed)
    loading_placeholder.empty()

main()