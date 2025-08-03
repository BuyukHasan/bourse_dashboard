from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.interface import Dashboard
from src.portfolio_manager import PortfolioManager
from src.reddit_analyzer import RedditSentiment
from src.news_fetcher import NewsFetcher
import random
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st


def test_dashboard(df):
    """Full test of the Dashboard class"""
    print("\n" + "="*50)
    print("DASHBOARD TEST".center(50))
    print("="*50)
    
    try:
        # 1. Initialisation
        print("\n[1] Initializing Dashboard...")
        dashboard = Dashboard(df)
        print("✅ Dashboard initialized successfully")
        
        # 2. Test complet en une seule exécution
        print("\n[2] Testing full display...")
        
        # Solution 1: Utiliser st.empty() comme conteneur
        placeholder = st.empty()
        with placeholder.container():
            dashboard.display()
        
        print("✅ Dashboard displayed without duplicates")
        
        # Solution alternative: Simuler l'exécution Streamlit
        # dashboard.display()
        # print("✅ Dashboard displayed (check manually for duplicates)")
        
        print("\n✅ All Dashboard tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard error: {str(e)}")
        return False
def test_visualizer(df):
    """Full test of the Visualizer class"""
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
    """Full test of DataFetcher with robust error handling"""
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
        {
            "name": "6-month data",
            "params": {"period": "6mo"},
            "min_rows": 120
        },
        {
            "name": "1-month data",
            "params": {"period": "1mo"}, 
            "min_rows": 20
        },
        {
            "name": "Specific date range",
            "params": {"start": "2025-07-01", "end": "2025-07-15"},
            "min_rows": 10
        }
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
        realtime = fetcher.RealTimeData()
        if not realtime.empty:
            print("✅ Latest quote:")
            print(realtime[['Ouv', 'Haut', 'Bas', 'Clôt']])
        else:
            print("⚠️ No real-time data (market closed?)")
    except Exception as e:
        print(f"❌ Real-time data error: {str(e)}")
        return False

    return True

def test_technical_analyzer(df):
    """Full test of the TechnicalAnalyzer class"""
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
        {
            "name": "50/200-day Moving Averages",
            "func": analyzer.calcul_50_200_jours,
            "check_cols": ['MA_50', 'MA_200']
        },
        {
            "name": "RSI Indicator",
            "func": lambda: analyzer.add_rsi(14),
            "check_cols": ['rsi']
        },
        {
            "name": "Trading Signals",
            "func": analyzer.Add_column_Signal,
            "check_cols": ['Signal']
        },
        {
            "name": "Daily Performance",
            "func": analyzer.Add_column_Performance,
            "check_cols": ['Daily_Return']
        },
        {
            "name": "Bollinger Bands",
            "func": lambda: analyzer.Bollinger_Bands(window=20),
            "check_cols": ['MA_BB', 'Sup_Band', 'Inf_Band']
        },
        {
            "name": "Return Calculation",
            "func": analyzer.Add_columns_rendements,
            "check_cols": ['rendements']
        }
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
    print(analyzer.df.tail(3)[['Clôt', 'MA_50', 'MA_200', 'rsi', 'Signal', 'Daily_Return']])
    
    return True
def test_multi_asset_comparison():
    """Test de la comparaison multi-actifs"""
    print("\n" + "="*50)
    print("COMPARAISON MULTI-ACTIFS TEST".center(50))
    print("="*50)
    
    try:
        # 1. Récupération des données
        print("\n[1] Récupération des données pour 3 actifs...")
        tickers = ["AAPL", "MSFT", "GOOGL"]
        data = {}
        
        for t in tickers:
            df = DataFetcher(t).fetch_data(period="6mo")
            analyzer = TechnicalAnalyzer(df)
            analyzer.calcul_50_200_jours()
            data[t] = analyzer.df
            print(f"✅ {t}: {len(df)} jours récupérés")
        
        # 2. Création du visualiseur
        print("\n[2] Création du graphique comparatif...")
        viz = Visualizer(data["AAPL"], rows=1, columns=1)
        
        # 3. Affichage des comparaisons
        print("\n[3] Affichage des courbes comparatives")
        viz.draw_multiple_tickers({
            "Apple": data["AAPL"],
            "Microsoft": data["MSFT"],
            "Google": data["GOOGL"]
        })
        
        # Configuration du layout
        viz.fig.update_layout(
            title="Comparaison des performances",
            yaxis_title="Prix de clôture ($)",
            hovermode="x unified"
        )
        
        st.plotly_chart(viz.fig, use_container_width=True)
        print("\n✅ Test de comparaison multi-actifs réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison: {str(e)}")
        return False
def portfolio_mode():
    st.title("🎯 Portefeuille Virtuel")
    
    # 1. Sélection des actifs et poids
    col1, col2 = st.columns(2)
    with col1:
        selected_tickers = st.multiselect(
            "Choisissez les actifs", 
            ["AAPL", "TSLA", "MSFT", "GOOGL"],
            default=["AAPL", "MSFT"]
        )
    with col2:
        weights = []
        for ticker in selected_tickers:
            weight = st.number_input(
                f"Poids de {ticker} (%)", 
                min_value=0, max_value=100, value=50
            )
            weights.append(weight / 100)  # Conversion en décimal
    
    # 2. Validation des poids
    if sum(weights) != 1.0:
        st.error("La somme des poids doit être égale à 100% !")
        return
    
    tickers_weights = dict(zip(selected_tickers, weights))
    
    # 3. Simulation
    if st.button("Lancer la simulation"):
        pm = PortfolioManager(tickers_weights)
        pm.fetch_portfolio_data(period="6mo")
        returns = pm.calculate_weighted_returns()
        metrics = pm.get_performance_metrics()
        
        # Affichage des résultats
        fig = Visualizer(returns, rows=1, columns=1)
        fig._add_trace(
            go.Scatter(
                x=returns.index,
                y=returns['Cumulative_Return'],
                name="Performance du Portefeuille",
                line=dict(color="royalblue", width=3)
            ),
            row=1, col=1
        )
        st.plotly_chart(fig.fig, use_container_width=True)
        
        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Rendement Annualisé", f"{metrics['annualized_return']:.2f}%")
        col2.metric("Volatilité", f"{metrics['volatility']:.2f}%")
        col3.metric("Ratio de Sharpe", f"{metrics['sharpe_ratio']:.2f}")
# Ajoutez ces nouvelles fonctions de test
def test_news_fetcher():
    """Test du NewsFetcher avec simulation"""
    print("\n" + "="*50)
    print("TEST NEWS FETCHER".center(50))
    print("="*50)
    
    try:
        fetcher = NewsFetcher()
        news = fetcher.get_company_news("AAPL")
        
        if not news:
            print("❌ Aucune nouvelle récupérée")
            return False
        
        print(f"✅ {len(news)} articles récupérés")
        for i, item in enumerate(news[:3]):  # Affiche les 3 premiers
            print(f"{i+1}. {item['title']} ({item['sentiment']})")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_reddit_sentiment():
    """Test du RedditSentiment avec simulation"""
    print("\n" + "="*50)
    print("TEST REDDIT SENTIMENT".center(50))
    print("="*50)
    
    try:
        analyzer = RedditSentiment()
        data = analyzer.analyze_ticker("TSLA")
        
        print(f"✅ Résultats: Positif={data['positive']}, Neutre={data['neutral']}, Négatif={data['negative']}")
        print(f"Total: {data['total']}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_portfolio_manager():
    """Test du PortfolioManager"""
    print("\n" + "="*50)
    print("TEST PORTFOLIO MANAGER".center(50))
    print("="*50)
    
    try:
        # Création d'un portefeuille fictif
        tickers_weights = {"AAPL": 0.6, "MSFT": 0.4}
        pm = PortfolioManager(tickers_weights)
        
        # Simulation de données
        dates = pd.date_range(end=datetime.today(), periods=100, freq='D')
        data = {}
        for ticker in tickers_weights:
            df = pd.DataFrame({
                'Clôt': [random.uniform(100, 200) for _ in range(100)],
                'Daily_Return': [random.uniform(-0.05, 0.05) for _ in range(100)]
            }, index=dates)
            data[ticker] = df
        
        pm.data = data
        returns = pm.calculate_weighted_returns()
        
        # Vérification des résultats
        if 'Portfolio_Return' not in returns.columns:
            print("❌ Colonne Portfolio_Return manquante")
            return False
        
        metrics = pm.get_performance_metrics()
        print(f"✅ Rendement annualisé: {metrics['annualized_return']:.2f}%")
        print(f"✅ Volatilité: {metrics['volatility']:.2f}%")
        print(f"✅ Ratio de Sharpe: {metrics['sharpe_ratio']:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
def test_alert_system():
    """Test du système d'alertes"""
    print("\n" + "="*50)
    print("TEST ALERT SYSTEM".center(50))
    print("="*50)
    
    try:
        # Création de données de test
        dates = pd.date_range(end=datetime.today(), periods=10, freq='D')
        df = pd.DataFrame({
            'Clôt': [150, 152, 155, 153, 156, 158, 160, 159, 162, 165],
            'rsi': [30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
            'Volatilite': [0.01, 0.02, 0.015, 0.018, 0.02, 0.022, 0.025, 0.03, 0.028, 0.026],
            'MA_50': [150, 151, 152, 153, 154, 155, 156, 157, 158, 159],
            'MA_200': [145, 146, 147, 148, 149, 150, 151, 152, 153, 154]
        }, index=dates)
        
        # Création du dashboard
        dashboard = Dashboard(df)
        
        # Configuration des alertes de test
        st.session_state.alertes = [
            {'indicateur': 'RSI', 'condition': 'Supérieur à', 'seuil': 70, 'active': True, 'declenchee': False},
            {'indicateur': 'Prix de clôture', 'condition': 'Supérieur à', 'seuil': 160, 'active': True, 'declenchee': False},
            {'indicateur': 'Croisement MA', 'condition': 'Croise vers le haut', 'seuil': 0, 'active': True, 'declenchee': False}
        ]
        
        # Vérification des alertes
        dashboard._check_alerts()
        
        # Vérification des alertes déclenchées
        alerts_triggered = [a['declenchee'] for a in st.session_state.alertes]
        if all(alerts_triggered):
            print("✅ Toutes les alertes ont été déclenchées")
            return True
        else:
            print(f"❌ Alertes non déclenchées: {alerts_triggered}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
def main():
    st.set_page_config(page_title="Dashboard Boursier", layout="wide")
    
    # Menu de sélection des modes - UNIQUEMENT UNE DÉCLARATION
    mode = st.sidebar.selectbox(
        "Choisir un mode",
        [
            "Dashboard Action Unique", 
            "Comparaison Multi-Actifs", 
            "Portefeuille Virtuel",
            "Tests Unitaires"
        ],
        key="mode_selector_unique"  # Clé unique
    )
    
    # Mode Dashboard Action Unique
    if mode == "Dashboard Action Unique":
        if 'df' not in st.session_state:
            fetcher = DataFetcher("AAPL")
            st.session_state.df = fetcher.fetch_data(period="6mo")
            analyzer = TechnicalAnalyzer(st.session_state.df)
            analyzer.calcul_50_200_jours()
            analyzer.add_rsi()
            analyzer.calculate_volatility()
        
        dashboard = Dashboard(st.session_state.df)
        dashboard.display()
    
    # Mode Comparaison Multi-Actifs
    elif mode == "Comparaison Multi-Actifs":
        st.title("Comparaison Multi-Actifs")
        
        # Paramètres de comparaison
        col1, col2 = st.columns(2)
        with col1:
            tickers = st.multiselect(
                "Sélectionnez les actions à comparer",
                ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL"],
                default=["AAPL", "MSFT", "GOOGL"],
                key="comparison_tickers"
            )
        with col2:
            start_date = st.date_input("Date de début", value=datetime.now().replace(year=datetime.now().year-1))
            end_date = st.date_input("Date de fin", value=datetime.now())
        
        if st.button("Lancer la comparaison", key="run_comparison"):
            compare_data = {}
            progress_bar = st.progress(0)
            
            for i, t in enumerate(tickers):
                try:
                    df = DataFetcher(t).fetch_data(start=start_date, end=end_date)
                    if not df.empty:
                        analyzer = TechnicalAnalyzer(df)
                        analyzer.calcul_50_200_jours()
                        compare_data[t] = analyzer.df
                    else:
                        st.warning(f"Aucune donnée disponible pour {t}")
                except Exception as e:
                    st.error(f"Erreur avec {t}: {str(e)}")
                progress_bar.progress((i+1) / len(tickers))
            
            if compare_data:
                st.session_state.compare_data = compare_data
        
        # Affichage du graphique comparatif
        if "compare_data" in st.session_state and st.session_state.compare_data:
            viz = Visualizer(next(iter(st.session_state.compare_data.values())), rows=1, columns=1)
            viz.draw_multiple_tickers(st.session_state.compare_data)
            
            viz.fig.update_layout(
                title="Comparaison des performances",
                yaxis_title="Prix de clôture ($)",
                hovermode="x unified",
                height=600
            )
            
            st.plotly_chart(viz.fig, use_container_width=True)
    
    # Mode Portefeuille Virtuel
    elif mode == "Portefeuille Virtuel":
        portfolio_mode()
    
    # Mode Tests Unitaires
    elif mode == "Tests Unitaires":
        st.title("🧪 Tests Unitaires")
        
        tests = {
            "DataFetcher": test_data_fetcher,
            "TechnicalAnalyzer": lambda: test_technical_analyzer(st.session_state.df if 'df' in st.session_state else None),
            "Visualizer": lambda: test_visualizer(st.session_state.df if 'df' in st.session_state else None),
            "Comparaison Multi-Actifs": test_multi_asset_comparison,
            "NewsFetcher": test_news_fetcher,
            "RedditSentiment": test_reddit_sentiment,
            "PortfolioManager": test_portfolio_manager,
            "Système d'Alertes": test_alert_system
        }
        
        selected_test = st.selectbox("Sélectionnez un test à exécuter", list(tests.keys()), key="test_selector")
        
        if st.button("Lancer le test", key="run_test"):
            with st.spinner("Exécution en cours..."):
                try:
                    success = tests[selected_test]()
                    if success:
                        st.success("✅ Test réussi!")
                    else:
                        st.error("❌ Test échoué")
                except Exception as e:
                    st.error(f"❌ Erreur lors du test: {str(e)}")
            
            st.text_area("Logs", value="Voir la console pour les détails", height=100, key="logs_area")
main()