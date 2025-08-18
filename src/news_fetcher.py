import random
import feedparser

class NewsFetcher:
    """Class to fetch company news"""
    
    def __init__(self):
        pass
    
    def get_company_news(self, ticker):
        """
        Get company news with sentiment simulation
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            list: News items with sentiment analysis
        """
        sentiment_map = {
            "positive": 0.8,   # Positive sentiment score
            "neutral": 0.2,    # Neutral sentiment score
            "negative": -0.5   # Negative sentiment score
        }
    
        try:
            feed = feedparser.parse(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}")
            return [{
                'title': entry.title,
                'source': "Yahoo Finance",
                'date': entry.published.split('T')[0],
                'url': entry.link,
                'sentiment': random.choice(["positive", "neutral", "negative"]),
                'score': sentiment_map[random.choice(["positive", "neutral", "negative"])]
            } for entry in feed.entries[:5]]
        except:
            return [{
                'title': f"Simulated news for {ticker}",
                'source': "System",
                'date': "2023-01-01",
                'url': "#",
                'sentiment': "neutral",
                'score': 0.2  # DEFAULT SCORE
            }]