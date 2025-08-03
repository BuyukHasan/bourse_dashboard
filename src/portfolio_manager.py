import pandas as pd
from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
import numpy as np
class PortfolioManager:
    def __init__(self, tickers_weights):
        """
        Initialise le gestionnaire de portefeuille avec des poids d'actifs.
        
        Args:
            tickers_weights (dict): Dictionnaire {ticker: poids} (ex: {"AAPL": 0.6, "MSFT": 0.4})
        """
        self.tw = tickers_weights
        self.data = {}  # Stocke les DataFrames par ticker
        self.returns = None  # DataFrame des rendements pondérés
    def fetch_portfolio_data(self, period="1y"):
        """
        Récupère les données pour tous les tickers du portefeuille.
        
        Args:
            period (str): Période historique (ex: "6mo", "1y")
        """
        for ticker in self.tw.keys():
            df = DataFetcher(ticker).fetch_data(period=period)
            analyzer = TechnicalAnalyzer(df)
            analyzer.Add_column_Performance()  # Ajoute les rendements journaliers
            self.data[ticker] = analyzer.df
    def calculate_weighted_returns(self):
        """
        Calcule les rendements journaliers pondérés du portefeuille.
        
        Returns:
            pd.DataFrame: DataFrame avec les colonnes:
                - 'Portfolio_Return' (rendement quotidien du portefeuille)
                - 'Cumulative_Return' (performance cumulée)
        """
        if not self.data:
            raise ValueError("Aucune donnée disponible. Exécutez fetch_portfolio_data() d'abord.")
        
        # Crée un DataFrame consolidé des rendements pondérés
        portfolio_returns = pd.DataFrame()
        
        for ticker, df in self.data.items():
            portfolio_returns[ticker] = df['Daily_Return'] * self.tw[ticker]
        
        # Somme des rendements pondérés
        portfolio_returns['Portfolio_Return'] = portfolio_returns.sum(axis=1)
        
        # Calcul du rendement cumulé
        portfolio_returns['Cumulative_Return'] = (
            (1 + portfolio_returns['Portfolio_Return']).cumprod() - 1
        ) * 100  # En pourcentage
        
        self.returns = portfolio_returns
        return portfolio_returns
    def get_performance_metrics(self):
        """
        Calcule les métriques clés du portefeuille.
        
        Returns:
            dict: {
                'annualized_return': float,
                'volatility': float,
                'sharpe_ratio': float
            }
        """
        if self.returns is None:
            raise ValueError("Exécutez calculate_weighted_returns() d'abord.")
        
        metrics = {}
        daily_returns = self.returns['Portfolio_Return']
        
        # Rendement annualisé
        metrics['annualized_return'] = ((1 + daily_returns.mean()) ** 252 - 1) * 100
        
        # Volatilité annualisée
        metrics['volatility'] = daily_returns.std() * np.sqrt(252) * 100
        
        # Ratio de Sharpe (suppose un taux sans risque de 0%)
        metrics['sharpe_ratio'] = (
            daily_returns.mean() / daily_returns.std() * np.sqrt(252)
        )
        
        return metrics
