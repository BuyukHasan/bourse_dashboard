import pandas as pd
import numpy as np

# Import local modules
from src.data_fetcher import DataFetcher

class TechnicalAnalyzer:
    """Class to perform technical analysis on financial data"""
    
    def __init__(self, data_frame):
        """
        Initialize analyzer with given DataFrame.
        
        Args:
            data_frame (pd.DataFrame): Data containing OHLC values.
        """
        required_columns = ['Open', 'High', 'Low', 'Close']
        if not all(col in data_frame.columns for col in required_columns):
            raise ValueError("Missing required columns")
        
        self.df = data_frame

    def show_dataframe(self):
        """Print current DataFrame (for debugging)"""
        print(self.df)

    def compute_50_200_days(self):
        """
        Compute 50-day and 200-day moving averages.
        Adds 'MA_50' and 'MA_200' columns to DataFrame.
        """
        if 'Close' not in self.df.columns:
            raise ValueError("Missing 'Close' column")

        self.df['MA_50'] = self.df['Close'].rolling(window=50).mean()
        self.df['MA_200'] = self.df['Close'].rolling(window=200).mean()
        self.df[['MA_50', 'MA_200']] = self.df[['MA_50', 'MA_200']].bfill()

    def add_rsi(self, window=14):
        """
        Add RSI (Relative Strength Index) indicator.
        
        Args:
            window (int): Number of periods for RSI calculation (default: 14)
        """
        delta = self.df['Close'].diff()
        gain = delta.where(delta > 0.0, 0)
        loss = -delta.where(delta < 0.0, 0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        self.df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss.mask(avg_loss == 0, 1))))

    def add_signal_column(self):
        """
        Add 'Signal' column based on MA_50/MA_200 crossover.
        Values:
            1 → Buy signal (MA_50 > MA_200)
           -1 → Sell signal (MA_50 < MA_200)
            0 → Neutral
        """
        required_columns = ['MA_50', 'MA_200']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Missing required columns")

        tolerance = 0.001
        diff = self.df['MA_50'] - self.df['MA_200']

        self.df['Signal'] = np.where(
            abs(diff) <= tolerance,
            0,
            np.where(diff > tolerance, 1, -1)
        )

    def add_performance_column(self):
        """Add 'Daily_Return' column (percentage daily return)."""
        self.df['Daily_Return'] = self.df['Close'].pct_change().fillna(0)

    def add_returns_columns(self):
        """Add 'returns' column (shifted signal * daily return)."""
        required_columns = ['Signal', 'Daily_Return']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Missing required columns")

        self.df['returns'] = self.df['Signal'].shift(1) * self.df['Daily_Return']

    def calculate_volatility(self, window=30, annualized=True):
        """
        Calculate volatility
        
        Args:
            window (int): Rolling window size (default: 30)
            annualized (bool): Annualize volatility (default: True)
        """
        returns = self.df['Close'].pct_change()
    
        # Verify sufficient data
        if len(returns) < window:
            # Use smaller window if needed
            window = max(2, len(returns) // 2)
        
        rolling_std = returns.rolling(window).std()
        
        if annualized:
            rolling_std = rolling_std * np.sqrt(252)  # Annualization
        
        self.df['Volatility'] = rolling_std

    def bollinger_bands(self, window=30, num_std=2):
        """
        Add Bollinger Bands to DataFrame.
        
        Args:
            window (int): Moving average window (default: 30)
            num_std (int): Standard deviations from mean (default: 2)
        """
        self.df['MA_BB'] = self.df['Close'].rolling(window).mean()
        if 'Volatility' not in self.df.columns:
            self.calculate_volatility(window=window)

        self.df['Upper_Band'] = self.df['MA_BB'] + num_std * self.df['Volatility']
        self.df['Lower_Band'] = self.df['MA_BB'] - num_std * self.df['Volatility']
        self._clean_data(self.df)

    def _clean_data(self, raw_data):
        """
        Clean and normalize input DataFrame.
        
        Args:
            raw_data (pd.DataFrame): Raw input data
            
        Returns:
            pd.DataFrame: Cleaned and formatted DataFrame
        """
        try:
            if raw_data.empty:
                print("Warning: Empty DataFrame received")
                return pd.DataFrame()

            cleaned = raw_data.rename(columns={
                "Open": "Open", "High": "High",
                "Low": "Low", "Close": "Close"
            })
            cleaned = cleaned.dropna()
            cleaned.index = pd.to_datetime(cleaned.index)
            return cleaned

        except Exception as e:
            print(f"Cleaning error: {str(e)}")
            return pd.DataFrame()
    
    @classmethod
    def test_analyzer(cls, df=None):
        """
        Test technical calculations
        
        Example:
        >>> df = DataFetcher.test_fetcher()
        >>> analyzer = TechnicalAnalyzer.test_analyzer(df)
        >>> print(analyzer.df[['MA_50', 'rsi']].tail())
        """
        if df is None:
            df = DataFetcher("AAPL").fetch_data(period="1mo")
    
        analyzer = cls(df)
        analyzer.compute_50_200_days()
        analyzer.add_rsi()
        return analyzer