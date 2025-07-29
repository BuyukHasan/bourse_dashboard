from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
import pandas as pd
from datetime import datetime

def tester_visualizer(df):
    """Test complet de la classe Visualizer"""
    print("\n" + "="*50)
    print("TEST VISUALIZER".center(50))
    print("="*50)
    
    try:
        # 1) Test basique 2x2 : prix + MA / RSI + zones
        print("\n[1] 2x2 : MA_draw + RSI_draw(show_zones=True)")
        viz1 = Visualizer(df, rows=2, columns=2, row_heights=[0.6, 0.4])
        viz1.MA_draw().Rsi_draw(show_zones=True).show()

        # 2) Test chandeliers et superposition MA
        print("\n[2] 2x2 : draw_candlestick + MA_draw(overlay=True) + RSI_draw")
        viz2 = Visualizer(df, rows=2, columns=2, row_heights=[0.6, 0.4])
        viz2.draw_candlestick() \
            .MA_draw(overlay=True) \
            .Rsi_draw(show_zones=True) \
            .show()

        # 3) Test volume + rendements cumulés dans un 3x1
        print("\n[3] 3x1 : chandeliers, volume, rendements cumulés")
        viz3 = Visualizer(df, rows=3, columns=1, row_heights=[0.5, 0.25, 0.25])
        viz3.draw_candlestick() \
            .draw_volume() \
            .draw_cumulative_returns() \
            .show()

        # 4) Test overlay multiple sur un seul subplot
        print("\n[4] 1x1 : toutes les traces en overlay")
        viz4 = Visualizer(df, rows=1, columns=1)
        viz4.draw_candlestick(overlay=True) \
            .MA_draw(overlay=True) \
            .Rsi_draw(show_zones=True, overlay=True) \
            .draw_volume(overlay=True) \
            .draw_cumulative_returns(overlay=True) \
            .show()

        # 5) Test reset_positions()
        print("\n[5] 2x2 + reset_positions() entre deux appels")
        viz5 = Visualizer(df, rows=2, columns=2)
        viz5.MA_draw()
        viz5.reset_position()
        viz5.Rsi_draw(show_zones=False)
        viz5.show()

        print("\n✅ Tous les tests Visualizer passés")
        return True

    except Exception as e:
        print(f"❌ Erreur dans Visualizer: {e}")
        return False
def tester_data_fetcher():
    """Test complet avec gestion améliorée des erreurs"""
    print("\n" + "="*50)
    print("TEST DATA_FETCHER".center(50))
    print("="*50)
    
    # 1. Initialisation
    try:
        print("\n[1] Initialisation...")
        fetcher = DataFetcher("TSLA")
        print(f"✅ Succès - Ticker: {fetcher.ticker}")
    except Exception as e:
        print(f"❌ Échec: {str(e)}")
        return False

    # 2. Test historique
    tests = [
        {
            "name": "Données 6 mois",
            "params": {"period": "6mo"},
            "min_rows": 120
        },
        {
            "name": "Données 1 mois",
            "params": {"period": "1mo"}, 
            "min_rows": 20
        },
        {
            "name": "Dates spécifiques",
            "params": {"start": "2025-07-01", "end": "2025-07-15"},
            "min_rows": 10
        }
    ]

    for test in tests:
        print(f"\n[2] Test {test['name']}...")
        try:
            df = fetcher.fetch_data(**test['params'])
            if df.empty:
                print(f"❌ Aucune donnée ({test['name']})")
                return False
            print(f"✅ Récupéré {len(df)} jours")
            print(f"Colonnes: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return False

    # 3. Test temps réel
    print("\n[3] Test données temps réel...")
    try:
        realtime = fetcher.RealTimeData()
        if not realtime.empty:
            print("✅ Dernier cours:")
            print(realtime[['Ouv', 'Haut', 'Bas', 'Clôt']])
        else:
            print("⚠️ Pas de données (marché fermé ?)")
    except Exception as e:
        print(f"❌ Erreur grave: {str(e)}")
        return False

    return True

def tester_technical_analyzer(df):
    """Test complet de la classe TechnicalAnalyzer"""
    print("\n" + "="*50)
    print("TEST TECHNICAL_ANALYZER".center(50))
    print("="*50)
    
    try:
        analyzer = TechnicalAnalyzer(df)
        print("✅ Initialisation réussie")
    except Exception as e:
        print(f"❌ Erreur initialisation: {str(e)}")
        return False

    # Liste des tests avec gestion d'erreur individuelle
    tests = [
        {
            "name": "Moyennes Mobiles 50/200j",
            "func": analyzer.calcul_50_200_jours,
            "check_cols": ['MA_50', 'MA_200']
        },
        {
            "name": "Indicateur RSI",
            "func": lambda: analyzer.add_rsi(14),
            "check_cols": ['rsi']
        },
        {
            "name": "Signaux de Trading",
            "func": analyzer.Add_column_Signal,
            "check_cols": ['Signal']
        },
        {
            "name": "Performance Quotidienne",
            "func": analyzer.Add_column_Performance,
            "check_cols": ['Daily_Return']
        },
        {
            "name": "Bandes de Bollinger",
            "func": lambda: analyzer.Bollinger_Bands(window=20),
            "check_cols": ['MA_BB', 'Sup_Band', 'Inf_Band']
        },
        {
            "name": "Calcul des Rendements",
            "func": analyzer.Add_columns_rendements,
            "check_cols": ['rendements']
        }
    ]

    for test in tests:
        print(f"\n➡️ Test: {test['name']}")
        try:
            test['func']()
            
            # Vérification des colonnes créées
            missing = [col for col in test['check_cols'] if col not in analyzer.df.columns]
            if missing:
                print(f"❌ Colonnes manquantes: {missing}")
            else:
                print(f"✅ Succès - Colonnes ajoutées: {test['check_cols']}")
                
        except Exception as e:
            print(f"❌ Erreur lors du test: {str(e)}")
            continue

    # Affichage des résultats finaux
    print("\n📊 Résumé des données analysées:")
    print(analyzer.df.tail(3)[['Clôt', 'MA_50', 'MA_200', 'rsi', 'Signal', 'Daily_Return']])
    
    return True

def main():
    print("\n" + "="*50)
    print("TEST COMPLET DU SYSTÈME".center(50))
    print("="*50)
    
    # Test DataFetcher
    if not tester_data_fetcher():
        print("\n❌ Correction nécessaire dans DataFetcher")
        return
        
    print("\n✅ Tous les tests DataFetcher passés")
    
    # Chargement des données
    fetcher = DataFetcher("AAPL")
    df = fetcher.fetch_data(period="1mo")
    
    if df.empty:
        print("\n❌ Impossible de charger des données pour TechnicalAnalyzer")
        return
    
    # Test TechnicalAnalyzer
    if not tester_technical_analyzer(df):
        print("\n❌ Correction nécessaire dans TechnicalAnalyzer")
        return
        
    print("\n✅ Tous les tests TechnicalAnalyzer passés")
    
    # Test Visualizer
    if not tester_visualizer(df):
        print("\n❌ Correction nécessaire dans Visualizer")
        return
        
    print("\n✅ Tous les tests Visualizer passés")
    print("\n🎉 Tous les tests ont été passés avec succès !")


main()