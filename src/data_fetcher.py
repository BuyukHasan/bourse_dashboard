import yfinance as yf
import pandas as pd

class DataFetcher:
    """Classe pour récupérer et prétraiter les données boursières."""
    
    def __init__(self, ticker="TSLA"):
        try : 
            self.ticker = ticker
            self.data = None
        except :
            print("Nom de l'action inconnu ou mal écrit")
    def fetch_data(self, period=None, start=None, end=None, interval="1d"):
        """Gère à la fois period (ex: '6mo') et start/end (ex: '2024-01-01')"""
        if period:
            data = yf.Ticker(self.ticker).history(period=period, interval=interval)
        else:
            data = yf.Ticker(self.ticker).history(start=start, end=end, interval=interval)
        return self._clean_data(data)
    def RealTimeData(self):
        """Version totalement robuste"""
        try:
            # 1. Récupération des données brutes
            raw_data = yf.Ticker(self.ticker).history(
                period="1d",
                interval="1m",
                timeout=10  # Timeout explicite
            )
        
            # 2. Vérification des données
            if raw_data is None or raw_data.empty:
                print("⚠️ Pas de données temps réel disponibles")
                return pd.DataFrame()
        
            # 3. Nettoyage avec vérification
            latest_data = raw_data.iloc[[-1]]  # Dernière minute
            cleaned_data = self._clean_data(latest_data)
        
            # Garantie de retour
            return cleaned_data if isinstance(cleaned_data, pd.DataFrame) else pd.DataFrame()
        
        except Exception as e:
            print(f"❌ Erreur temps réel: {str(e)}")
            return pd.DataFrame()  # Retour garanti
    def _clean_data(self, raw_data):
        """Garantit toujours un DataFrame en retour"""
        try:
            if raw_data is None or raw_data.empty:
                return pd.DataFrame()
            
            # Copie pour éviter les modifications inattendues
            cleaned = raw_data.copy()
        
            # Renommage sécurisé
            cleaned = cleaned.rename(columns={
                "Open": "Ouv",
                "High": "Haut",
                "Low": "Bas",
                "Close": "Clôt"
            })
        
            # Nettoyage
            cleaned = cleaned.dropna()
            if not cleaned.empty:
                cleaned.index = pd.to_datetime(cleaned.index)
        
            return cleaned
        
        except Exception as e:
            print(f"⚠️ Erreur nettoyage: {str(e)}")
            return pd.DataFrame()