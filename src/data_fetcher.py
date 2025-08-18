import yfinance as yf
import pandas as pd
from datetime import datetime

class DataFetcher:
    """Fetch and preprocess stock market data"""
    
    def __init__(self, ticker="TSLA"):
        """
        Initialize data fetcher
        
        Args:
            ticker (str): Stock ticker symbol (default: "TSLA")
        """
        try:
            self.ticker = ticker
            self.data = None
        except:
            print("⚠️ Unknown or misspelled ticker symbol")

    def fetch_data(self, period=None, start=None, end=None, interval="1d", timeout=10):
        """
        Fetch historical market data
        
        Args:
            period (str): Data period (e.g., "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            start (str/datetime): Start date (YYYY-MM-DD)
            end (str/datetime): End date (YYYY-MM-DD)
            interval (str): Data interval (default: "1d")
            timeout (int): Request timeout in seconds (default: 10)
        
        Returns:
            pd.DataFrame: Cleaned historical data
        """
        # Date conversion
        if start is not None:
            if isinstance(start, (pd.Timestamp, datetime)):
                start = start.strftime("%Y-%m-%d")
        
        if end is not None:
            if isinstance(end, (pd.Timestamp, datetime)):
                end = end.strftime("%Y-%m-%d")
        
        # Special treatment for bond ETFs
        bond_etfs = ["TLT", "IEF", "LQD", "HYG", "BND", "GOVT", "VGIT", "VGLT"]
        
        try:
            if self.ticker in bond_etfs:
                bond_ticker = self.ticker + ".BO" if not self.ticker.endswith(".BO") else self.ticker
                # Priority to specific dates
                if start and end:
                    data = yf.Ticker(bond_ticker).history(
                        start=start,
                        end=end,
                        interval=interval
                    )
                else:
                    # Fallback to period
                    data = yf.Ticker(bond_ticker).history(
                        period=period,
                        interval=interval
                    )
            else:
                # Standard treatment - priority to specific dates
                if start and end:
                    data = yf.Ticker(self.ticker).history(
                        start=start,
                        end=end,
                        interval=interval,
                        timeout=timeout
                    )
                else:
                    # Fallback to period
                    data = yf.Ticker(self.ticker).history(
                        period=period,
                        interval=interval,
                        timeout=timeout
                    )
            
            cleaned = self._clean_data(data)
            
            # Check if data is empty
            if cleaned.empty:
                print(f"⚠️ No data found for {self.ticker} (start={start}, end={end}, period={period})")
            
            return cleaned
            
        except Exception as e:
            print(f"❌ Critical error with {self.ticker}: {str(e)}")
            return pd.DataFrame()

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