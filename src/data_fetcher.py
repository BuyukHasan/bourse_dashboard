import yfinance as yf
import pandas as pd

class DataFetcher:
    """Class to fetch and preprocess stock market data."""
    
    def __init__(self, ticker="TSLA"):
        try:
            self.ticker = ticker
            self.data = None
        except:
            print("⚠️ Unknown or misspelled ticker symbol")

    def fetch_data(self, period=None, start=None, end=None, interval="1d"):
        """
        Fetch historical market data for a given ticker.

        Args:
            period (str): e.g., '6mo', '1y'. If provided, overrides start/end.
            start (str): Start date in 'YYYY-MM-DD' format.
            end (str): End date in 'YYYY-MM-DD' format.
            interval (str): Data interval (e.g., '1d', '1h', '1m').

        Returns:
            pd.DataFrame: Cleaned and formatted historical data.
        """
        if period:
            data = yf.Ticker(self.ticker).history(period=period, interval=interval)
        else:
            data = yf.Ticker(self.ticker).history(start=start, end=end, interval=interval)
        
        return self._clean_data(data)

    def RealTimeData(self):
        """
        Fetches the most recent real-time data (1-minute interval).

        Returns:
            pd.DataFrame: Latest price data (1 row), or empty DataFrame on failure.
        """
        try:
            raw_data = yf.Ticker(self.ticker).history(
                period="1d",
                interval="1m",
                timeout=10  # Explicit timeout
            )

            if raw_data is None or raw_data.empty:
                print("⚠️ No real-time data available")
                return pd.DataFrame()

            latest_data = raw_data.iloc[[-1]]  # Only the latest timestamp
            cleaned_data = self._clean_data(latest_data)

            return cleaned_data if isinstance(cleaned_data, pd.DataFrame) else pd.DataFrame()

        except Exception as e:
            print(f"❌ Real-time data error: {str(e)}")
            return pd.DataFrame()

    def _clean_data(self, raw_data):
        """
        Internal method to clean raw data fetched from Yahoo Finance.

        Args:
            raw_data (pd.DataFrame): Raw data from yfinance.

        Returns:
            pd.DataFrame: Cleaned DataFrame with renamed columns and parsed dates.
        """
        try:
            if raw_data is None or raw_data.empty:
                return pd.DataFrame()

            cleaned = raw_data.copy()

            # Rename columns to match internal convention
            cleaned = cleaned.rename(columns={
                "Open": "Ouv",
                "High": "Haut",
                "Low": "Bas",
                "Close": "Clôt"
            })

            cleaned = cleaned.dropna()
            if not cleaned.empty:
                cleaned.index = pd.to_datetime(cleaned.index)

            return cleaned

        except Exception as e:
            print(f"⚠️ Cleaning error: {str(e)}")
            return pd.DataFrame()
    def test_fetcher(cls):
        """Teste la classe DataFetcher
    
        Exemple:
        >>> df = DataFetcher.test_fetcher()
        >>> print(df[['Ouv', 'Clôt']].head())
        >>> print("\n✅ Test fetch_data OK")
        """
        fetcher = cls("AAPL")
        df = fetcher.fetch_data(period="1mo")
        assert not df.empty, "Erreur: DataFrame vide"
        return df