import streamlit as st
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer

class Dashboard:
    def __init__(self):
        self.tickers = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL"]
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)