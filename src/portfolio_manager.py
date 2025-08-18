import pandas as pd
import numpy as np
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import local modules
from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.geo_data import GeoDataFetcher

class PortfolioManager:
    """Class to manage virtual portfolios"""
    
    def __init__(self, tickers_weights):
        """
        Initialize portfolio manager with asset weights.
        
        Args:
            tickers_weights (dict): {ticker: weight} dictionary (ex: {"AAPL": 0.6, "MSFT": 0.4})
        """
        self.weights = tickers_weights
        self.data = {}  # Stores DataFrames by ticker
        self.returns = None  # DataFrame of weighted returns
        
    def get_combined_geo_influence(self):
        """Calculate combined geographical influence for portfolio"""
        geo_fetcher = GeoDataFetcher()
        country_weights = {}
        
        # Aggregate weights by country
        for ticker, weight in self.weights.items():
            geo_data = geo_fetcher.get_geo_data(ticker)
            for item in geo_data:
                country = item['country']
                country_weights[country] = country_weights.get(country, 0) + (item['weight'] * weight)
        
        # Normalize to sum to 1
        total = sum(country_weights.values())
        if total > 0:
            for country in country_weights:
                country_weights[country] /= total
        
        # Prepare for visualization
        combined_data = []
        for country, weight in country_weights.items():
            if country in geo_fetcher.country_data:
                combined_data.append({
                    "country": country,
                    "weight": weight,
                    **geo_fetcher.country_data[country]
                })
        
        return combined_data
        
    def fetch_portfolio_data(self, period="1y"):
        """Fetch portfolio data with improved error handling"""
        def fetch_and_process(ticker):
            try:
                df = DataFetcher(ticker).fetch_data(period=period)
                if df.empty:
                    return ticker, None, f"No data for {ticker}"
                    
                analyzer = TechnicalAnalyzer(df)
                analyzer.add_performance_column()
                return ticker, analyzer.df, None
            except Exception as e:
                return ticker, None, str(e)

        data = {}
        errors = {}
        
        # Limit to 4 concurrent requests max
        max_workers = min(4, len(self.weights))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for t in self.weights.keys():
                future = executor.submit(
                    fetch_and_process, 
                    t
                )
                futures[future] = t
            
            results = []
            for i, future in enumerate(as_completed(futures)):
                t = futures[future]
                try:
                    t, df, error = future.result()
                    if error:
                        errors[t] = error
                    elif df is not None:
                        data[t] = df
                except Exception as e:
                    errors[t] = str(e)
                    
        return data, errors
        
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
        
    def calculate_correlations(self):
        """Calculate correlations between portfolio assets"""
        closes = pd.DataFrame()
        for ticker, df in self.data.items():
            if not df.empty:
                closes[ticker] = df['Close']
        
        if closes.empty:
            return pd.DataFrame()
        
        return closes.corr()