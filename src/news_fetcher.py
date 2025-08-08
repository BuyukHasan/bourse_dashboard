import random
import feedparser

class NewsFetcher:
    def __init__(self):
        pass
    
    # Update get_company_news method
    def get_company_news(self, ticker):
        sentiment_map = {
            "positif": 0.8,   # Positive sentiment score
            "neutre": 0.2,    # Neutral sentiment score
            "négatif": -0.5   # Negative sentiment score
        }
    
        try:
            feed = feedparser.parse(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}")
            return [{
            'title': entry.title,
            'source': "Yahoo Finance",
            'date': entry.published.split('T')[0],
            'url': entry.link,
            'sentiment': random.choice(["positif", "neutre", "négatif"]),
            'score': sentiment_map[random.choice(["positif", "neutre", "négatif"])]  # ADD THIS LINE
            } for entry in feed.entries[:5]]
        except:
            return [{
            'title': f"Nouvelles simulées pour {ticker}",
            'source': "Système",
            'date': "2023-01-01",
            'url': "#",
            'sentiment': "neutre",
            'score': 0.2  # DEFAULT SCORE
            }]