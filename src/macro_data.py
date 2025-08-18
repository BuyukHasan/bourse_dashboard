import pandas as pd
import yfinance as yf
import streamlit as st

class MacroData:
    INDICATORS = {
        "VIX": "^VIX",  # Indice de volatilité
        "Treasury 10Y": "^TNX",  # Rendement obligataire
        "Pétrole Brent": "BZ=F",  # Matière première
        "Or": "GC=F",
        "Dollar Index": "DX=F",
        "Bitcoin": "BTC-USD",
        "S&P 500": "^GSPC"
    }

    @st.cache_data(ttl=3600, show_spinner=False)
    def fetch_macro_data(_self, period="1y"):
        macro_df = pd.DataFrame()
        errors = {}  # Nouveau: stocke les erreurs par indicateur
        
        for name, ticker in _self.INDICATORS.items():
            try:
                # Changement ici: utiliser yf.download()
                data = yf.download(ticker, period=period, progress=False)
                
                if data.empty:
                    errors[name] = "No data"
                    continue
                    
                macro_df[name] = data['Close']
                
            except Exception as e:
                errors[name] = str(e)
        
        return macro_df, errors

    def get_correlation(self, stock_data, macro_df):
        """Calcule la corrélation entre un actif et les indicateurs macro"""
        if macro_df.empty or stock_data.empty:
            return pd.DataFrame()
            
        merged = pd.merge(stock_data, macro_df, left_index=True, right_index=True, how='inner')
        corr_matrix = merged.corr()
        return corr_matrix[['Close']].sort_values('Close', ascending=False)