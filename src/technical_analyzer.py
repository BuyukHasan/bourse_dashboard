from src.data_fetcher import DataFetcher
import pandas as pd
import numpy as np

class TechnicalAnalyzer:

    def __init__(self, data_frame):
        """
        Initialize the analyzer with the given DataFrame.

        Args:
            data_frame (pd.DataFrame): Data containing OHLC values.
        """
        required_columns = ['Ouv', 'Haut', 'Bas', 'Clôt']
        if not all(col in data_frame.columns for col in required_columns):
            raise ValueError("Missing required columns")
        
        self.df = data_frame

    def show_dataframe(self):
        """Print the current DataFrame (for debugging purposes)."""
        print(self.df)

    def calcul_50_200_jours(self):
        """
        Compute 50-day and 200-day moving averages.
        Adds columns 'MA_50' and 'MA_200' to the DataFrame.
        """
        if 'Clôt' not in self.df.columns:
            raise ValueError("Missing 'Clôt' column")

        self.df['MA_50'] = self.df['Clôt'].rolling(window=50).mean()
        self.df['MA_200'] = self.df['Clôt'].rolling(window=200).mean()
        self.df[['MA_50', 'MA_200']] = self.df[['MA_50', 'MA_200']].fillna(method='bfill')

    def add_rsi(self, window=14):
        """
        Add RSI (Relative Strength Index) indicator to the DataFrame.

        Args:
            window (int): Number of periods for RSI calculation.
        """
        delta = self.df['Clôt'].diff()
        gain = delta.where(delta > 0.0, 0)
        loss = -delta.where(delta < 0.0, 0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        self.df['rsi'] = 100 - (100 / (1 + (avg_gain / avg_loss.mask(avg_loss == 0, 1))))

    def Add_column_Signal(self):
        """
        Add a 'Signal' column based on crossover between MA_50 and MA_200.
        Values:
            1  → Buy signal (MA_50 > MA_200)
           -1  → Sell signal (MA_50 < MA_200)
            0  → Neutral
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

    def Add_column_Performance(self):
        """
        Add a 'Daily_Return' column to the DataFrame,
        representing percentage daily return.
        """
        self.df['Daily_Return'] = self.df['Clôt'].pct_change().fillna(0)

    def Add_columns_rendements(self):
        """
        Add a 'rendements' column to the DataFrame.
        Computed as shifted signal * daily return.
        """
        required_columns = ['Signal', 'Daily_Return']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Missing required columns")

        self.df['rendements'] = self.df['Signal'].shift(1) * self.df['Daily_Return']

    def calculate_volatility(self, window=30, annualized=True):
        """
        Calculate rolling volatility (standard deviation of returns).

        Args:
            window (int): Rolling window size.
            annualized (bool): Whether to annualize volatility.
        """
        returns = self.df['Clôt'].pct_change()
        self.df['Volatilite'] = returns.rolling(window).std() * (np.sqrt(252) if annualized else 1)

    def Bollinger_Bands(self, window=30, num_std=2):
        """
        Add Bollinger Bands to the DataFrame.

        Args:
            window (int): Moving average window.
            num_std (int): Number of standard deviations from the mean.
        """
        self.df['MA_BB'] = self.df['Clôt'].rolling(window).mean()
        if 'Volatilite' not in self.df.columns:
            self.calculate_volatility(window=window)

        self.df['Sup_Band'] = self.df['MA_BB'] + num_std * self.df['Volatilite']
        self.df['Inf_Band'] = self.df['MA_BB'] - num_std * self.df['Volatilite']
        self._clean_data(self.df)

    def _clean_data(self, raw_data):
        """
        Clean and normalize the input DataFrame.

        Args:
            raw_data (pd.DataFrame): Raw input data.

        Returns:
            pd.DataFrame: Cleaned and formatted DataFrame.
        """
        try:
            if raw_data.empty:
                print("Warning: Empty DataFrame received")
                return pd.DataFrame()

            cleaned = raw_data.rename(columns={
                "Open": "Ouv", "High": "Haut",
                "Low": "Bas", "Close": "Clôt"
            })
            cleaned = cleaned.dropna()
            cleaned.index = pd.to_datetime(cleaned.index)
            return cleaned

        except Exception as e:
            print(f"Cleaning error: {str(e)}")
            return pd.DataFrame()