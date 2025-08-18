from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.dashboard import Dashboard
from src.portfolio_manager import PortfolioManager
from src.reddit_analyzer import RedditSentiment
from src.news_fetcher import NewsFetcher
from src.css import Cssdash  
from src.geo_data import GeoDataFetcher
from src.asset_categories import AssetCategories
import random
import pandas as pd
import time
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
import tempfile
import os

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
    if st.session_state.get('theme') == "Crypto Fever":
        st.markdown("""
        <div class="block-animation">
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
            <div class="block"></div>
        </div>
        """, unsafe_allow_html=True)

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
    
    # Réinitialiser l'état du portfolio à chaque entrée dans le mode
    if 'portfolio_results' in st.session_state:
        del st.session_state.portfolio_results
    
    # Catégories d'actifs étendues
    asset_categories = AssetCategories.get_all_categories()
    
    # Nouvelle interface multi-colonnes pour la sélection des actifs
    st.subheader("📌 Sélection des actifs par secteur")
    
    # Créer 3 colonnes pour afficher les secteurs
    cols = st.columns(3)
    selected_tickers = []
    
    # Afficher chaque catégorie dans une colonne
    for i, category in enumerate(asset_categories.keys()):
        with cols[i % 3]:
            tickers = st.multiselect(
                f"{category}",
                asset_categories[category],
                key=f"cat_{category}"
            )
            selected_tickers.extend(tickers)
    
    if not selected_tickers:
        st.warning("Veuillez sélectionner au moins un actif")
        return
    
    # Section pour les poids
    st.subheader("📊 Définir les poids des actifs")
    
    # Calculer le poids par défaut (répartition égale)
    default_weight = 100 // len(selected_tickers) if selected_tickers else 0
    
    # Créer 4 colonnes pour les poids
    weight_cols = st.columns(4)
    weights = []
    
    for i, ticker in enumerate(selected_tickers):
        with weight_cols[i % 4]:
            weight = st.slider(
                f"Poids de {ticker} (%)",
                0, 100, 
                value=default_weight,
                key=f"weight_{ticker}"
            )
            weights.append(weight)
    
    # Vérifier et normaliser les poids
    total_weight = sum(weights)
    
    if abs(total_weight - 100) > 1:
        st.warning(f"⚠️ La somme des poids est {total_weight}%. Normalisation automatique appliquée.")
        normalized_weights = [round((w / total_weight) * 100, 2) for w in weights]
    else:
        normalized_weights = weights
    
    # Afficher les poids normalisés
    with st.expander("Voir la répartition finale des poids"):
        for ticker, weight in zip(selected_tickers, normalized_weights):
            st.write(f"- {ticker}: {weight:.2f}%")
    
    # Créer le dictionnaire tickers/poids
    tickers_weights = dict(zip(selected_tickers, [w/100 for w in normalized_weights]))
    
    if st.button("Lancer la simulation", key="run_portfolio_sim"):
        # Réinitialiser les résultats précédents
        if 'portfolio_results' in st.session_state:
            del st.session_state.portfolio_results
        
        with st.status("**Construction du portefeuille...**", expanded=True) as status:
            pm = PortfolioManager(tickers_weights)
            
            status.write("⏳ Téléchargement des données...")
            try:
                data, errors = pm.fetch_portfolio_data(period="6mo")
                pm.data = data
                
                # Afficher les erreurs
                if errors:
                    for t, err in errors.items():
                        status.warning(f"{t}: {err}")
                        
                # Vérifier qu'on a au moins 2 jeux de données
                if len(data) < 2:
                    status.error("❌ Insuffisant de données pour la simulation")
                    st.stop()
            except Exception as e:
                status.error(f"Erreur de récupération des données : {str(e)}")
                st.stop()
            
            # Étape 2: Calcul des rendements pondérés
            status.write("⏳ Calcul des rendements pondérés...")
            try:
                returns = pm.calculate_weighted_returns()
            except Exception as e:
                status.error(f"Erreur de calcul des rendements : {str(e)}")
                st.stop()
            
            # Étape 3: Calcul des métriques de performance
            status.write("⏳ Calcul des performances...")
            try:
                metrics = pm.get_performance_metrics()
            except Exception as e:
                status.error(f"Erreur de calcul des performances : {str(e)}")
                st.stop()
            
            # Étape 4: Calcul de l'influence géographique combinée
            status.write("⏳ Analyse de l'influence géographique...")
            try:
                geo_data = pm.get_combined_geo_influence()
            except Exception as e:
                status.warning(f"Attention : {str(e)}")
                geo_data = None
            
            st.session_state.portfolio_results = {
                'returns': returns,
                'metrics': metrics,
                'geo_data': geo_data
            }
            status.update(label="Simulation terminée !", state="complete")
        
        if 'portfolio_results' in st.session_state:
            results = st.session_state.portfolio_results
            returns = results['returns']
            metrics = results['metrics']
            geo_data = results['geo_data']
            
            # Création du graphique de performance
            if not returns.empty:
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
                fig.fig.update_layout(
                    title="Performance cumulative du portefeuille",
                    yaxis_title="Rendement cumulé (%)",
                    hovermode="x unified"
                )
                st.plotly_chart(fig.fig, use_container_width=True)
            else:
                st.warning("Aucune donnée de rendement disponible")
            
            # Affichage des métriques de performance
            st.subheader("📈 Métriques de performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Rendement annualisé", f"{metrics.get('annualized_return', 0):.2f}%")
            col2.metric("Volatilité", f"{metrics.get('volatility', 0):.2f}%")
            col3.metric("Ratio de Sharpe", f"{metrics.get('sharpe_ratio', 0):.2f}")
            
            # Affichage de l'influence géographique
            st.subheader("🌍 Influence Géographique Combinée")
            
            if geo_data:
                df_geo = pd.DataFrame(geo_data)
                df_geo['size'] = df_geo['weight'] * 50
                
                fig = px.scatter_geo(
                    df_geo,
                    lat='lat',
                    lon='lon',
                    size='size',
                    color='weight',
                    color_continuous_scale='Viridis',
                    hover_name='country',
                    hover_data={'weight': ':.2%', 'lat': False, 'lon': False, 'size': False},
                    projection='natural earth',
                    title="Influence Géographique du Portefeuille"
                )
                
                fig.update_layout(
                    geo=dict(
                        bgcolor='rgba(0,0,0,0)',
                        landcolor='lightgray',
                        showcountries=True,
                        countrycolor='gray'
                    ),
                    margin=dict(l=0, r=0, t=40, b=0),
                    coloraxis_colorbar=dict(title="Influence", tickformat=".0%")
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tableau détaillé
                with st.expander("Détails par pays"):
                    st.dataframe(
                        df_geo[['country', 'weight']].sort_values('weight', ascending=False),
                        column_config={
                            "country": "Pays",
                            "weight": st.column_config.ProgressColumn(
                                "Influence",
                                format="%.2f%%",
                                min_value=0,
                                max_value=1
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
            else:
                st.warning("Aucune donnée géographique disponible pour ce portefeuille")
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

@st.cache_data(ttl=600, show_spinner=False)
def load_initial_data(ticker="AAPL", period="6mo"):
    fetcher = DataFetcher(ticker)
    df = fetcher.fetch_data(period=period)
    analyzer = TechnicalAnalyzer(df)
    analyzer.compute_50_200_days()
    analyzer.add_rsi()
    analyzer.calculate_volatility()
    analyzer.add_signal_column()
    analyzer.add_performance_column()
    analyzer.add_returns_columns()
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

@st.cache_data(ttl=3600, show_spinner=False, hash_funcs={pd.Timestamp: lambda _: None})
def fetch_single_ticker_data(ticker, start_date, end_date):
    """Fonction threadée avec cache pour récupérer les données d'un ticker"""
    try:
        # Utiliser une clé de cache unique basée sur les paramètres
        cache_key = f"{ticker}_{start_date}_{end_date}"
        
        # Vérifier si les données sont déjà en cache
        if cache_key in st.session_state.get('ticker_cache', {}):
            return ticker, st.session_state.ticker_cache[cache_key]
        
        fetcher = DataFetcher(ticker)
        df = fetcher.fetch_data(start=start_date, end=end_date)
        
        if not df.empty:
            analyzer = TechnicalAnalyzer(df)
            analyzer.compute_50_200_days()
            analyzer.add_rsi()
            analyzer.calculate_volatility()
            analyzer.add_signal_column()
            analyzer.add_performance_column()
            analyzer.add_returns_columns()
            
            # Mettre en cache
            if 'ticker_cache' not in st.session_state:
                st.session_state.ticker_cache = {}
            st.session_state.ticker_cache[cache_key] = analyzer.df
            
            return ticker, analyzer.df
        return ticker, None
    except Exception as e:
        return ticker, str(e)
def clear_yfinance_cache():
    cache_dir = os.path.join(tempfile.gettempdir(), 'yfinance')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)

clear_yfinance_cache()
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
        theme_names = ["Neon Cyberpunk", "Lava Explosion", "Electric Ocean", 
                       "Acid Jungle", "Galactic Purple","Retro Dark","Crypto Fever"]
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
                    <div class="triangle"></div>
                    <div class="eye"></div>
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
        # Initialiser les dates par défaut
        default_start = datetime.now().replace(year=datetime.now().year-1)
        default_end = datetime.now()
        
        # Récupérer les dates du sélecteur
        start_date = st.sidebar.date_input("Date de début:", value=default_start)
        end_date = st.sidebar.date_input("Date de fin:", value=default_end)
        
        # Charger les données avec les dates sélectionnées
        if 'df' not in st.session_state or st.session_state.get('last_dates') != (start_date, end_date):
            with st.spinner("Chargement des données..."):
                fetcher = DataFetcher("AAPL")
                df = fetcher.fetch_data(start=start_date, end=end_date)
                
                if not df.empty:
                    analyzer = TechnicalAnalyzer(df)
                    analyzer.compute_50_200_days()
                    analyzer.add_rsi()
                    analyzer.calculate_volatility()
                    analyzer.add_signal_column()
                    analyzer.add_performance_column()
                    analyzer.add_returns_columns()
                    st.session_state.df = analyzer.df
                    st.session_state.last_dates = (start_date, end_date)
                else:
                    st.error("Aucune donnée disponible pour cette période")
                    return
        
        if 'df' in st.session_state:
            dashboard = Dashboard(st.session_state.df)
            dashboard.display()
    
    elif mode == "Comparaison multi-actifs":
        st.title("Comparaison multi-actifs")
        
        # Catégories d'actifs pour la comparaison
        asset_categories = AssetCategories.get_all_categories()
        
        # Créer une liste unique de tous les tickers
        all_tickers = []
        for category in asset_categories:
            all_tickers.extend(asset_categories[category])
            
        all_tickers = list(set(all_tickers))
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
            
            with st.status("**Chargement des données...**", expanded=True) as status:
                st.write("Initialisation du téléchargement des données boursières")
                progress_bar = st.progress(0)
                status_container = st.container()
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {}
                    for t in tickers:
                        future = executor.submit(
                            fetch_single_ticker_data, 
                            t, 
                            start_date, 
                            end_date
                        )
                        futures[future] = t
                    
                    results = []
                    for i, future in enumerate(as_completed(futures)):
                        t = futures[future]
                        progress = (i + 1) / len(tickers)
                        progress_bar.progress(progress)
                        
                        try:
                            ticker, result = future.result()
                            if isinstance(result, pd.DataFrame):
                                compare_data[ticker] = result
                                status_container.success(f"✅ {ticker} chargé avec succès")
                            elif result is None:
                                status_container.warning(f"⚠️ Aucune donnée disponible pour {ticker}")
                            else:
                                status_container.error(f"❌ Erreur avec {ticker}: {result}")
                        except Exception as e:
                            status_container.error(f"❌ Erreur critique avec {ticker}: {str(e)}")
                
                if compare_data:
                    st.session_state.compare_data = compare_data
                    status.update(label="Données chargées avec succès !", state="complete")
                else:
                    status.update(label="Échec du chargement des données", state="error")
        
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
    # Ajouter un bouton pour vider le cache
    with st.sidebar.expander("Options avancées"):
        if st.button("Vider le cache", help="Force le rechargement de toutes les données"):
            st.cache_data.clear()
            if 'ticker_cache' in st.session_state:
                del st.session_state.ticker_cache
            if 'data_cache' in st.session_state:
                del st.session_state.data_cache
            st.rerun()
main()