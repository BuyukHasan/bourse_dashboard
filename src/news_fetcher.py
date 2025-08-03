import random
import feedparser

class NewsFetcher:
    def __init__(self):
        pass
    
    def get_company_news(self, ticker):
        """Nouvelles simulées avec Yahoo Finance RSS"""
        try:
            feed = feedparser.parse(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}")
            return [{
                'title': entry.title,
                'source': "Yahoo Finance",
                'date': entry.published.split('T')[0],
                'url': entry.link,
                'sentiment': random.choice(["positif", "neutre", "négatif"])
            } for entry in feed.entries[:5]]  # Limite à 5 articles
        except:
            # Fallback statique si Yahoo échoue
            return [{
                'title': f"Nouvelles simulées pour {ticker}",
                'source': "Système",
                'date': "2023-01-01",
                'url': "#",
                'sentiment': "neutre"
            }]