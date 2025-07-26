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
    def add_rsi(self , window = 14) :

        delta = self.df['Clôt'].diff()

        gain = delta.where(delta > 0.0 , 0)
        loss = -delta.where(delta < 0.0 , 0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        self.df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss.replace(0, 1))))