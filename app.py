from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer

fetcher = DataFetcher("TSLA")
df = fetcher.fetch_data()

analyze = TechnicalAnalyzer(df)
analyze.calcul_50_200_jours()
analyze.show_dataframe()