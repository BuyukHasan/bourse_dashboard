import yfinance as yf
import pandas as pd

class DataFetcher:
    """Fetch and preprocess stock market data"""
    
    def __init__(self, ticker="TSLA"):
        try:
            self.ticker = ticker
            self.data = None
        except:
            print("⚠️ Unknown or misspelled ticker symbol")

    def fetch_data(self, period=None, start=None, end=None, interval="1d"):
        # Convertir les dates en string si ce sont des objets datetime
        if isinstance(start, pd.Timestamp):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, pd.Timestamp):
            end = end.strftime("%Y-%m-%d")
        # Traitement spécial pour les ETF obligataires
        bond_etfs = ["TLT", "IEF", "LQD", "HYG", "BND", "GOVT", "VGIT", "VGLT"]
        
        if self.ticker in bond_etfs:
            bond_ticker = self.ticker + ".BO" if not self.ticker.endswith(".BO") else self.ticker
            data = yf.Ticker(bond_ticker).history(
                period=period,
                interval=interval,
                start=start,
                end=end
            )
        else:
            # Traitement standard
            data = yf.Ticker(self.ticker).history(
                period=period,
                interval=interval,
                start=start,
                end=end
            )
        
        return self._clean_data(data)

    def real_time_data(self):
        """
        Fetch most recent real-time data (1-minute interval)
        Returns:
            pd.DataFrame: Latest price data (1 row) or empty DataFrame
        """
        try:
            raw_data = yf.Ticker(self.ticker).history(
                period="1d",
                interval="1m",
                timeout=10
            )

            if raw_data is None or raw_data.empty:
                print("⚠️ No real-time data available")
                return pd.DataFrame()

            latest_data = raw_data.iloc[[-1]]
            cleaned_data = self._clean_data(latest_data)

            return cleaned_data if isinstance(cleaned_data, pd.DataFrame) else pd.DataFrame()

        except Exception as e:
            print(f"❌ Real-time data error: {str(e)}")
            return pd.DataFrame()

    def _clean_data(self, raw_data):
        """
        Clean raw Yahoo Finance data
        Args:
            raw_data (pd.DataFrame): Raw data
        Returns:
            pd.DataFrame: Cleaned DataFrame with parsed dates
        """
        try:
            if raw_data is None or raw_data.empty:
                return pd.DataFrame()

            cleaned = raw_data.copy()
            cleaned = cleaned.rename(columns={
                "Open": "Open",
                "High": "High",
                "Low": "Low",
                "Close": "Close"
            })

            cleaned = cleaned.dropna()
            if not cleaned.empty:
                cleaned.index = pd.to_datetime(cleaned.index)

            return cleaned

        except Exception as e:
            print(f"⚠️ Cleaning error: {str(e)}")
            return pd.DataFrame()
    
    @classmethod
    def test_fetcher(cls):
        """
        Test DataFetcher class
        Example:
        >>> df = DataFetcher.test_fetcher()
        >>> print(df[['Open', 'Close']].head())
        """
        fetcher = cls("AAPL")
        df = fetcher.fetch_data(period="1mo")
        assert not df.empty, "Error: Empty DataFrame"
        return df