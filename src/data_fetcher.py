import yfinance as yf
import pandas as pd

class DataFetcher:
    """Classe pour récupérer et prétraiter les données boursières."""
    
    def __init__(self, ticker="TSLA"):
        self.ticker = ticker
        self.data = None
    def fetch_data(self, start="2023-01-01", end="2024-01-01"):
        """Récupère les données historiques et les prétraite."""
        raw_data = yf.Ticker(self.ticker).history(start=start, end=end)
        self._clean_data(raw_data)
        return self.data
    def _clean_data(self, raw_data):
        """Nettoyage interne des données."""
        self.data = raw_data.rename(columns={
            "Open": "Ouv", "High": "Haut", 
            "Low": "Bas", "Close": "Clôt"
        })
        self.data.dropna(inplace=True)
        self.data.index = pd.to_datetime(self.data.index)

# Exemple d'utilisation
if __name__ == "__main__":
    fetcher = DataFetcher("TSLA")
    df = fetcher.fetch_data()
    print(df.tail())