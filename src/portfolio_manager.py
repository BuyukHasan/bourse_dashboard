import pandas as pd
from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import streamlit as st

class PortfolioManager:
    def __init__(self, tickers_weights):
        """
        Initialize portfolio manager with asset weights.
        
        Args:
            tickers_weights (dict): {ticker: weight} dictionary (ex: {"AAPL": 0.6, "MSFT": 0.4})
        """
        self.weights = tickers_weights
        self.data = {}  # Stores DataFrames by ticker
        self.returns = None  # DataFrame of weighted returns
    
    def fetch_portfolio_data(self, period="1y", status_container=None):
        """
        Fetch data for all portfolio tickers using threading with visual feedback.
        """
        def fetch_and_process(ticker):
            try:
                df = DataFetcher(ticker).fetch_data(period=period)
                analyzer = TechnicalAnalyzer(df)
                analyzer.add_performance_column()
                return ticker, analyzer.df
            except Exception as e:
                if status_container:
                    status_container.error(f"Erreur avec {ticker}: {str(e)}")
                return ticker, None

        if status_container:
            status_container.write("⏳ Téléchargement des données des actifs...")
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_and_process, t): t for t in self.weights.keys()}
            
            for i, future in enumerate(as_completed(futures)):
                ticker = futures[future]
                ticker, df = future.result()
                
                if df is not None:
                    self.data[ticker] = df
                    if status_container:
                        status_container.success(f"✅ {ticker} chargé")
                else:
                    if status_container:
                        status_container.warning(f"⚠️ Échec du chargement pour {ticker}")
    
    def calculate_weighted_returns(self):
        """
        Calculate weighted daily portfolio returns.
        
        Returns:
            pd.DataFrame: DataFrame with columns:
                - 'Portfolio_Return' (daily portfolio return)
                - 'Cumulative_Return' (cumulative performance)
        """
        if not self.data:
            raise ValueError("No data available. Run fetch_portfolio_data() first.")
        
        # Create consolidated DataFrame of weighted returns
        portfolio_returns = pd.DataFrame()
        
        for ticker, df in self.data.items():
            portfolio_returns[ticker] = df['Daily_Return'] * self.weights[ticker]
        
        # Sum of weighted returns
        portfolio_returns['Portfolio_Return'] = portfolio_returns.sum(axis=1)
        
        # Calculate cumulative return
        portfolio_returns['Cumulative_Return'] = (
            (1 + portfolio_returns['Portfolio_Return']).cumprod() - 1
        ) * 100  # In percentage
        
        self.returns = portfolio_returns
        return portfolio_returns
    
    def get_performance_metrics(self):
        """
        Calculate key portfolio metrics.
        
        Returns:
            dict: {
                'annualized_return': float,
                'volatility': float,
                'sharpe_ratio': float
            }
        """
        if self.returns is None:
            raise ValueError("Run calculate_weighted_returns() first.")
        
        metrics = {}
        daily_returns = self.returns['Portfolio_Return']
        
        # Annualized return
        metrics['annualized_return'] = ((1 + daily_returns.mean()) ** 252 - 1) * 100
        
        # Annualized volatility
        metrics['volatility'] = daily_returns.std() * np.sqrt(252) * 100
        
        # Sharpe ratio (assumes 0% risk-free rate)
        metrics['sharpe_ratio'] = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
        
        return metrics