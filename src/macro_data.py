import pandas as pd
import yfinance as yf
import streamlit as st

class MacroData:
    """Class to fetch macroeconomic data"""
    
    INDICATORS = {
        "VIX": "^VIX",  # Volatility index
        "Treasury 10Y": "^TNX",  # Bond yield
        "Brent Oil": "BZ=F",  # Commodity
        "Gold": "GC=F",
        "Dollar Index": "DX=F",
        "Bitcoin": "BTC-USD",
        "S&P 500": "^GSPC"
    }

    @st.cache_data(ttl=3600, show_spinner=False)
    def fetch_macro_data(_self, period="1y"):
        """
        Fetch macroeconomic data with caching
        
        Args:
            period (str): Data period (default: "1y")
            
        Returns:
            tuple: (DataFrame of macro data, dictionary of errors)
        """
        macro_df = pd.DataFrame()
        errors = {}  # Store errors by indicator
        
        for name, ticker in _self.INDICATORS.items():
            try:
                # Use yf.download()
                data = yf.download(ticker, period=period, progress=False)
                
                if data.empty:
                    errors[name] = "No data"
                    continue
                    
                macro_df[name] = data['Close']
                
            except Exception as e:
                errors[name] = str(e)
        
        return macro_df, errors

    def get_correlation(self, stock_data, macro_df):
        """
        Calculate correlation between asset and macro indicators
        
        Args:
            stock_data (pd.DataFrame): Stock price data
            macro_df (pd.DataFrame): Macroeconomic data
            
        Returns:
            pd.DataFrame: Correlation matrix
        """
        if macro_df.empty or stock_data.empty:
            return pd.DataFrame()
            
        merged = pd.merge(stock_data, macro_df, left_index=True, right_index=True, how='inner')
        corr_matrix = merged.corr()
        return corr_matrix[['Close']].sort_values('Close', ascending=False)