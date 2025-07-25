from src.data_fetcher import DataFetcher

fetcher = DataFetcher("TSLA")
df = fetcher.fetch_data()
print(df)