from src.data_fetcher import DataFetcher
import pandas as pd
import numpy as np

class TechnicalAnalyzer :

    def __init__(self, data_frame):
        # Vérification des colonnes nécessaires
        required_columns = ['Ouv', 'Haut', 'Bas', 'Clôt']
        if not all(col in data_frame.columns for col in required_columns):
            raise ValueError("Il manque des colonnes nécessaires")
        
        self.df = data_frame
    
    def show_dataframe(self):
        print(self.df)
    def calcul_50_200_jours(self):
        # Vérifie que la colonne Clôt existe
        if 'Clôt' not in self.df.columns:
            raise ValueError("La colonne 'Clôt' est manquante")
        
        # Calcul des moyennes mobiles
        self.df['MA_50'] = self.df['Clôt'].rolling(window=50).mean()
        self.df['MA_200'] = self.df['Clôt'].rolling(window=200).mean()
        self.df[['MA_50', 'MA_200']] = self.df[['MA_50', 'MA_200']].fillna(method='bfill')  # Remplissage des NaN résiduels
    def add_rsi(self , window = 14) :

        delta = self.df['Clôt'].diff()

        gain = delta.where(delta > 0.0 , 0)
        loss = -delta.where(delta < 0.0 , 0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        self.df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss.mask(avg_loss == 0, 1))))
    def Add_column_Signal(self) : 
        # Vérification des colonnes nécessaires
        required_columns = ['MA_50' , 'MA_200']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Il manque des colonnes nécessaires")
        tolerance = 0.001  # Seuil pour considérer l'égalité
        diff = self.df['MA_50'] - self.df['MA_200']
    
        self.df['Signal'] = np.where(
            abs(diff) <= tolerance,
            0,  # Neutre si différence négligeable
            np.where(
                diff > tolerance,
                1,   # Achat si MA50 > MA200 (avec marge)
                -1    # Vente si MA50 < MA200
            )
        )
    def Add_column_Performance(self):
        self.df['Daily_Return'] = self.df['Clôt'].pct_change()
        self.df['Daily_Return'] = self.df['Daily_Return'].fillna(0)

    def Add_columns_rendements(self) :
        # Vérification des colonnes nécessaires
        required_columns = ['Signal' , 'Daily_Return']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Il manque des colonnes nécessaires")
        self.df['rendements'] = self.df['Signal'].shift(1) * self.df['Daily_Return']
    def calculate_volatility(self, window=30, annualized=True):
        """Centralise tous les calculs de volatilité"""
        returns = self.df['Clôt'].pct_change()
        self.df['Volatilite'] = returns.rolling(window).std() * (np.sqrt(252) if annualized else 1)

    def Bollinger_Bands(self, window=30, num_std=2):
        """Version cohérente avec calculate_volatility()"""
        # 1. Calculer la MM et la volatilité ensemble
        self.df['MA_BB'] = self.df['Clôt'].rolling(window).mean()
        if 'Volatilite' not in self.df.columns:
            self.calculate_volatility(window=window)  # Même fenêtre pour cohérence
    
        # 2. Calcul des bandes
        self.df['Sup_Band'] = self.df['MA_BB'] + num_std * self.df['Volatilite']
        self.df['Inf_Band'] = self.df['MA_BB'] - num_std * self.df['Volatilite']
        self._clean_data(self.df) 
    def _clean_data(self, raw_data):
        """Version robuste qui retourne toujours un DataFrame"""
        try:
            if raw_data.empty:
                print("Avertissement: DataFrame vide reçu")
                return pd.DataFrame()
            
            cleaned = raw_data.rename(columns={
                "Open": "Ouv", "High": "Haut", 
                "Low": "Bas", "Close": "Clôt"
            })
            cleaned = cleaned.dropna()
            cleaned.index = pd.to_datetime(cleaned.index)
            return cleaned  # Retour explicite
        
        except Exception as e:
            print(f"Erreur nettoyage: {str(e)}")
            return pd.DataFrame()  # Retourne un DataFrame vide au lieu de None