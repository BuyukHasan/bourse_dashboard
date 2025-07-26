from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
fetcher = DataFetcher("TSLA")
df = fetcher.fetch_data()

analyze = TechnicalAnalyzer(df)
analyze.calcul_50_200_jours()
analyze.add_rsi()
analyze.show_dataframe()

visualizer = Visualizer(df)
visualizer.MA_draw()
visualizer.Rsi_draw()
visualizer.overpurchaseselling()
visualizer.show_graph()