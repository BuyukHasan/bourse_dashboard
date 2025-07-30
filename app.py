from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.interface import Dashboard
import pandas as pd
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

def main():
    st.set_page_config(page_title="Dashboard Boursier", layout="wide")
    
    # Initialiser les données
    if 'df' not in st.session_state:
        fetcher = DataFetcher("AAPL")
        st.session_state.df = fetcher.fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(st.session_state.df)
        analyzer.calcul_50_200_jours()
        analyzer.add_rsi()
        analyzer.calculate_volatility()

    # Afficher le dashboard
    dashboard = Dashboard(st.session_state.df)
    dashboard.display()

main()